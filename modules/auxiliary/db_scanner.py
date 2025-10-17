"""Database service scanner and fingerprinting module"""

import socket
import re
from urllib.parse import urlparse
from colorama import Fore, Style
from modules.base import BaseModule

class DatabaseScanner(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Database service detection and fingerprinting"
        self.module_type = "auxiliary"
        self.options = {
            "TARGET": "",
            "TIMEOUT": "5",
        }
        self.required_options = ["TARGET"]
        
        self.db_ports = {
            1433: "Microsoft SQL Server",
            1434: "Microsoft SQL Server Browser",
            3306: "MySQL",
            5432: "PostgreSQL",
            27017: "MongoDB",
            27018: "MongoDB Shard",
            27019: "MongoDB Config",
            6379: "Redis",
            7000: "Cassandra",
            7001: "Cassandra JMX",
            9042: "Cassandra CQL",
            8529: "ArangoDB",
            28015: "RethinkDB",
            5984: "CouchDB",
            9200: "Elasticsearch",
            50000: "DB2",
            1521: "Oracle",
            2483: "Oracle",
            2484: "Oracle",
        }
        
        self.db_banners = {
            b'mysql': 'MySQL',
            b'postgres': 'PostgreSQL',
            b'MongoDB': 'MongoDB',
            b'Redis': 'Redis',
            b'Microsoft SQL': 'Microsoft SQL Server',
            b'Oracle': 'Oracle Database',
        }
    
    def run(self):
        target = self.get_option("TARGET")
        timeout = int(self.get_option("TIMEOUT"))
        
        parsed = urlparse(target if '://' in target else f'http://{target}')
        hostname = parsed.hostname or parsed.path.split('/')[0]
        
        print(f"{Fore.YELLOW}[*] Scanning database services on: {hostname}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        detected_services = []
        
        for port, service_name in self.db_ports.items():
            print(f"{Fore.CYAN}[*] Checking port {port} ({service_name})...{Style.RESET_ALL}", end='\r')
            
            if self._check_port(hostname, port, timeout):
                banner = self._grab_banner(hostname, port, timeout)
                db_type = self._identify_database(banner, service_name)
                
                detected_services.append({
                    "port": port,
                    "service": service_name,
                    "type": db_type,
                    "banner": banner[:100] if banner else "No banner"
                })
                
                print(f"{Fore.GREEN}[+] FOUND: {service_name} on port {port} (Type: {db_type}){Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        
        if detected_services:
            print(f"{Fore.GREEN}[+] Detected {len(detected_services)} database services:{Style.RESET_ALL}\n")
            for service in detected_services:
                print(f"{Fore.CYAN}  Port {service['port']}: {service['service']} ({service['type']}){Style.RESET_ALL}")
                if service['banner'] != "No banner":
                    print(f"{Fore.YELLOW}    Banner: {service['banner'][:80]}...{Style.RESET_ALL}")
            print()
            
            return {
                "success": True,
                "message": f"Detected {len(detected_services)} database services",
                "services": detected_services
            }
        else:
            print(f"{Fore.YELLOW}[*] No database services detected{Style.RESET_ALL}\n")
            return {
                "success": True,
                "message": "No database services detected"
            }
    
    def _check_port(self, hostname: str, port: int, timeout: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((hostname, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _grab_banner(self, hostname: str, port: int, timeout: int) -> str:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((hostname, port))
            
            try:
                sock.send(b'\n')
            except Exception:
                pass
            
            banner = sock.recv(1024)
            sock.close()
            
            return banner.decode('utf-8', errors='ignore')
        except Exception:
            return ""
    
    def _identify_database(self, banner: str, default_service: str) -> str:
        if not banner:
            return default_service
        
        banner_bytes = banner.encode('utf-8', errors='ignore')
        
        for pattern, db_name in self.db_banners.items():
            if pattern in banner_bytes:
                return db_name
        
        return default_service
