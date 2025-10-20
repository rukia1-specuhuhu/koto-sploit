"""Logging system for Kotosploit"""

import logging
import os
import sys
import json
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from colorama import Fore, Style
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SysLogHandler
import threading
import queue
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class KotosploitLogger:
    def __init__(self, log_dir: str = "./logs", log_level: str = "INFO", 
                 max_file_size: int = 10*1024*1024, backup_count: int = 5,
                 enable_async: bool = True, enable_syslog: bool = False,
                 syslog_address: str = '/dev/log'):
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.enable_async = enable_async
        self.enable_syslog = enable_syslog
        self.syslog_address = syslog_address
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"kotosploit_{timestamp}.log")
        self.json_log_file = os.path.join(log_dir, f"kotosploit_{timestamp}.json")
        
        self.session_id = timestamp
        self.session_start = datetime.now()
        
        self._setup_loggers()
        
        if enable_async:
            self.log_queue = queue.Queue()
            self.log_thread = threading.Thread(target=self._async_log_worker, daemon=True)
            self.log_thread.start()
        else:
            self.log_queue = None
            self.log_thread = None
        
        self.email_config = None
        self.webhook_config = None
        
        self.stats = {
            "debug": 0,
            "info": 0,
            "warning": 0,
            "error": 0,
            "critical": 0,
            "modules_executed": 0,
            "vulnerabilities_found": 0,
            "scans_started": 0,
            "scans_completed": 0
        }
    
    def _setup_loggers(self):
        self.logger = logging.getLogger("Kotosploit")
        self.logger.setLevel(self.log_level)
        self.logger.handlers = []
        
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        file_handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=self.max_file_size, 
            backupCount=self.backup_count
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        json_handler = RotatingFileHandler(
            self.json_log_file, 
            maxBytes=self.max_file_size, 
            backupCount=self.backup_count
        )
        json_handler.setLevel(self.log_level)
        json_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(json_handler)
        
        if self.enable_syslog:
            try:
                syslog_handler = SysLogHandler(address=self.syslog_address)
                syslog_handler.setLevel(logging.WARNING)
                self.logger.addHandler(syslog_handler)
            except Exception as e:
                self.logger.warning(f"Failed to setup syslog handler: {e}")
    
    def _async_log_worker(self):
        while True:
            try:
                log_func, args, kwargs = self.log_queue.get(timeout=0.1)
                log_func(*args, **kwargs)
                self.log_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"{Fore.RED}[!] Logging error: {e}{Style.RESET_ALL}")
    
    def _log(self, level, message: str, color: str = None, **kwargs):
        self.stats[level.lower()] += 1
        
        if color:
            print(f"{color}[{level.upper()}] {message}{Style.RESET_ALL}")
        
        if self.enable_async and self.log_queue:
            self.log_queue.put((getattr(self.logger, level.lower()), (message,), kwargs))
        else:
            getattr(self.logger, level.lower())(message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log("DEBUG", message, Fore.CYAN, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log("INFO", message, Fore.WHITE, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log("WARNING", message, Fore.YELLOW, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log("ERROR", message, Fore.RED, **kwargs)
        
        if 'exc_info' not in kwargs:
            self.error(message, exc_info=True, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log("CRITICAL", message, Fore.RED + Style.BRIGHT, **kwargs)
        
        if self.email_config and self.email_config.get("notify_on_critical"):
            self._send_alert_email("Critical Alert", message)
        
        if self.webhook_config and self.webhook_config.get("notify_on_critical"):
            self._send_webhook_alert("critical", message)
    
    def exception(self, message: str, **kwargs):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        full_message = f"{message}\n{tb_str}"
        
        self._log("ERROR", full_message, Fore.RED, **kwargs)
    
    def log_module_execution(self, module_name: str, target: str, result: str, 
                           execution_time: float = None, options: Dict[str, Any] = None):
        self.stats["modules_executed"] += 1
        
        log_data = {
            "event_type": "module_execution",
            "module": module_name,
            "target": target,
            "result": result,
            "execution_time": execution_time,
            "options": options or {},
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        
        message = f"Module: {module_name} | Target: {target} | Result: {result}"
        if execution_time:
            message += f" | Time: {execution_time:.2f}s"
        
        self.info(message, extra={"log_data": log_data})
    
    def log_vulnerability_found(self, vuln_type: str, target: str, payload: str, 
                              severity: str = "Medium", description: str = None,
                              evidence: str = None, module: str = None):
        self.stats["vulnerabilities_found"] += 1
        
        log_data = {
            "event_type": "vulnerability_found",
            "vulnerability_type": vuln_type,
            "target": target,
            "payload": payload,
            "severity": severity,
            "description": description,
            "evidence": evidence,
            "module": module,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        
        message = f"VULNERABILITY FOUND - Type: {vuln_type} | Severity: {severity} | Target: {target} | Payload: {payload}"
        if description:
            message += f" | Description: {description}"
        
        self.critical(message, extra={"log_data": log_data})
    
    def log_scan_start(self, scan_type: str, target: str, options: Dict[str, Any] = None):
        self.stats["scans_started"] += 1
        
        log_data = {
            "event_type": "scan_start",
            "scan_type": scan_type,
            "target": target,
            "options": options or {},
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        
        message = f"Starting {scan_type} scan on {target}"
        self.info(message, extra={"log_data": log_data})
    
    def log_scan_complete(self, scan_type: str, target: str, findings: int, 
                        execution_time: float = None):
        self.stats["scans_completed"] += 1
        
        log_data = {
            "event_type": "scan_complete",
            "scan_type": scan_type,
            "target": target,
            "findings": findings,
            "execution_time": execution_time,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        
        message = f"Completed {scan_type} scan on {target} - Found {findings} issues"
        if execution_time:
            message += f" | Time: {execution_time:.2f}s"
        
        self.info(message, extra={"log_data": log_data})
    
    def log_request(self, method: str, url: str, status_code: int, 
                  response_time: float, data_size: int = None):
        log_data = {
            "event_type": "http_request",
            "method": method,
            "url": url,
            "status_code": status_code,
            "response_time": response_time,
            "data_size": data_size,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id
        }
        
        message = f"HTTP {method} {url} - Status: {status_code} | Time: {response_time:.3f}s"
        if data_size:
            message += f" | Size: {data_size} bytes"
        
        self.debug(message, extra={"log_data": log_data})
    
    def configure_email_alerts(self, smtp_server: str, smtp_port: int, username: str, 
                             password: str, to_email: str, from_email: str = None,
                             notify_on_critical: bool = True, notify_on_error: bool = False):
        self.email_config = {
            "smtp_server": smtp_server,
            "smtp_port": smtp_port,
            "username": username,
            "password": password,
            "to_email": to_email,
            "from_email": from_email or username,
            "notify_on_critical": notify_on_critical,
            "notify_on_error": notify_on_error
        }
    
    def configure_webhook_alerts(self, webhook_url: str, notify_on_critical: bool = True,
                               notify_on_error: bool = False, headers: Dict[str, str] = None):
        self.webhook_config = {
            "webhook_url": webhook_url,
            "headers": headers or {"Content-Type": "application/json"},
            "notify_on_critical": notify_on_critical,
            "notify_on_error": notify_on_error
        }
    
    def _send_alert_email(self, subject: str, message: str):
        if not self.email_config:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config["from_email"]
            msg['To'] = self.email_config["to_email"]
            msg['Subject'] = f"[Kotosploit Alert] {subject}"
            
            body = f"""
            <p><strong>Kotosploit Security Framework Alert</strong></p>
            <p><strong>Session ID:</strong> {self.session_id}</p>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Alert:</strong> {message}</p>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"]) as server:
                server.starttls()
                server.login(self.email_config["username"], self.email_config["password"])
                server.send_message(msg)
            
            self.info(f"Alert email sent to {self.email_config['to_email']}")
        except Exception as e:
            self.error(f"Failed to send alert email: {e}")
    
    def _send_webhook_alert(self, level: str, message: str):
        if not self.webhook_config:
            return
        
        try:
            import requests
            
            payload = {
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id,
                "level": level,
                "message": message,
                "source": "Kotosploit"
            }
            
            response = requests.post(
                self.webhook_config["webhook_url"],
                json=payload,
                headers=self.webhook_config["headers"],
                timeout=10
            )
            
            if response.status_code == 200:
                self.info(f"Webhook alert sent successfully")
            else:
                self.warning(f"Webhook returned status code: {response.status_code}")
        except Exception as e:
            self.error(f"Failed to send webhook alert: {e}")
    
    def get_session_stats(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "session_start": self.session_start.isoformat(),
            "session_duration": str(datetime.now() - self.session_start),
            "log_counts": self.stats.copy(),
            "log_file": self.log_file,
            "json_log_file": self.json_log_file
        }
    
    def print_session_summary(self):
        stats = self.get_session_stats()
        
        print(f"\n{Fore.YELLOW}Session Logging Summary{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Session ID: {stats['session_id']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Duration: {stats['session_duration']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Log file: {stats['log_file']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}JSON log file: {stats['json_log_file']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Debug: {stats['log_counts']['debug']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Info: {stats['log_counts']['info']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Warning: {stats['log_counts']['warning']}{Style.RESET_ALL}")
        print(f"{Fore.RED}Error: {stats['log_counts']['error']}{Style.RESET_ALL}")
        print(f"{Fore.RED + Style.BRIGHT}Critical: {stats['log_counts']['critical']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Modules executed: {stats['log_counts']['modules_executed']}{Style.RESET_ALL}")
        print(f"{Fore.RED + Style.BRIGHT}Vulnerabilities found: {stats['log_counts']['vulnerabilities_found']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Scans started: {stats['log_counts']['scans_started']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Scans completed: {stats['log_counts']['scans_completed']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
    
    def close(self):
        if self.log_thread and self.log_thread.is_alive():
            self.log_queue.join()
        
        self.info(f"Logging session ended. Duration: {datetime.now() - self.session_start}")
        self.print_session_summary()

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'log_data') and isinstance(record.log_data, dict):
            log_record.update(record.log_data)
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_record)
