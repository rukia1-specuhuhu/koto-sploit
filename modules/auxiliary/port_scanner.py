"""Port scanner module"""

import socket
from urllib.parse import urlparse
from colorama import Fore, Style
from modules.base import BaseModule

class PortScanner(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "TCP port scanner for common ports"
        self.module_type = "auxiliary"
        self.options = {
            "TARGET": "",
            "PORTS": "common",
            "TIMEOUT": "2",
        }
        self.required_options = ["TARGET"]
        
        self.common_ports = {
            20: "FTP Data",
            21: "FTP Control",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            6379: "Redis",
            8080: "HTTP Proxy",
            8443: "HTTPS Alt",
            27017: "MongoDB",
        }
    
    def run(self):
        target = self.get_option("TARGET")
        ports_option = self.get_option("PORTS")
        timeout = int(self.get_option("TIMEOUT"))
        
        parsed = urlparse(target if '://' in target else f'http://{target}')
        hostname = parsed.hostname or parsed.path.split('/')[0]
        
        print(f"{Fore.YELLOW}[*] Target: {hostname}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Port scan mode: {ports_option}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        if ports_option == "common":
            ports = list(self.common_ports.keys())
        else:
            try:
                if '-' in ports_option:
                    start, end = map(int, ports_option.split('-'))
                    ports = list(range(start, end + 1))
                else:
                    ports = [int(p.strip()) for p in ports_option.split(',')]
            except Exception:
                print(f"{Fore.RED}[!] Invalid port specification{Style.RESET_ALL}")
                return {"success": False, "message": "Invalid port specification"}
        
        open_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((hostname, port))
                sock.close()
                
                if result == 0:
                    service = self.common_ports.get(port, "Unknown")
                    open_ports.append((port, service))
                    print(f"{Fore.GREEN}[+] Port {port} OPEN ({service}){Style.RESET_ALL}")
                else:
                    print(f"{Fore.CYAN}[-] Port {port} closed{Style.RESET_ALL}", end='\r')
            except Exception:
                pass
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        
        if open_ports:
            print(f"{Fore.GREEN}[+] Found {len(open_ports)} open ports:{Style.RESET_ALL}\n")
            for port, service in open_ports:
                print(f"{Fore.CYAN}  Port {port}: {service}{Style.RESET_ALL}")
            print()
            return {
                "success": True,
                "message": f"Found {len(open_ports)} open ports",
                "open_ports": open_ports
            }
        else:
            print(f"{Fore.YELLOW}[*] No open ports found{Style.RESET_ALL}\n")
            return {
                "success": True,
                "message": "No open ports found"
            }
