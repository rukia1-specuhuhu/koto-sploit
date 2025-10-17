"""Logging system for Kotosploit"""

import logging
import os
from datetime import datetime
from colorama import Fore, Style

class KotosploitLogger:
    def __init__(self, log_dir: str = "./logs", log_level: str = "INFO"):
        self.log_dir = log_dir
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"kotosploit_{timestamp}.log")
        
        logging.basicConfig(
            level=self.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("Kotosploit")
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)
    
    def critical(self, message: str):
        self.logger.critical(message)
    
    def log_module_execution(self, module_name: str, target: str, result: str):
        log_message = f"Module: {module_name} | Target: {target} | Result: {result}"
        self.info(log_message)
    
    def log_vulnerability_found(self, vuln_type: str, target: str, payload: str):
        log_message = f"VULNERABILITY FOUND - Type: {vuln_type} | Target: {target} | Payload: {payload}"
        self.critical(log_message)
        print(f"{Fore.RED}[VULN] {log_message}{Style.RESET_ALL}")
    
    def log_scan_start(self, scan_type: str, target: str):
        log_message = f"Starting {scan_type} scan on {target}"
        self.info(log_message)
    
    def log_scan_complete(self, scan_type: str, target: str, findings: int):
        log_message = f"Completed {scan_type} scan on {target} - Found {findings} issues"
        self.info(log_message)
