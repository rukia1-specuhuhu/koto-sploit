"""SSL/TLS vulnerability scanner module"""

import requests
import ssl
import socket
from urllib.parse import urlparse
from colorama import Fore, Style
from modules.base import BaseModule

class SSLScanner(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "SSL/TLS configuration and vulnerability scanner"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "TIMEOUT": "10",
        }
        self.required_options = ["URL"]
    
    def run(self):
        url = self.get_option("URL")
        timeout = int(self.get_option("TIMEOUT"))
        
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.path
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        
        print(f"{Fore.YELLOW}[*] Scanning SSL/TLS configuration for: {hostname}:{port}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        results = {
            "hostname": hostname,
            "port": port,
            "issues": [],
            "protocols": [],
            "ciphers": []
        }
        
        print(f"{Fore.CYAN}[*] Testing SSL/TLS protocols...{Style.RESET_ALL}\n")
        
        protocols = [
            ("SSLv2", ssl.PROTOCOL_SSLv23),
            ("SSLv3", ssl.PROTOCOL_SSLv23),
            ("TLSv1.0", ssl.PROTOCOL_TLSv1),
            ("TLSv1.1", ssl.PROTOCOL_TLSv1_1),
            ("TLSv1.2", ssl.PROTOCOL_TLSv1_2),
        ]
        
        try:
            if hasattr(ssl, 'PROTOCOL_TLSv1_3'):
                protocols.append(("TLSv1.3", ssl.PROTOCOL_TLSv1_3))
        except AttributeError:
            pass
        
        for proto_name, proto_const in protocols:
            try:
                context = ssl.SSLContext(proto_const)
                with socket.create_connection((hostname, port), timeout=timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        results["protocols"].append(proto_name)
                        print(f"{Fore.GREEN}[+] {proto_name}: SUPPORTED{Style.RESET_ALL}")
                        
                        if proto_name in ["SSLv2", "SSLv3", "TLSv1.0"]:
                            issue = f"Weak protocol {proto_name} is supported"
                            results["issues"].append(issue)
                            print(f"{Fore.RED}    [!] WARNING: {issue}{Style.RESET_ALL}")
            except Exception:
                print(f"{Fore.YELLOW}[-] {proto_name}: NOT SUPPORTED{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}[*] Testing HTTPS certificate...{Style.RESET_ALL}\n")
        
        try:
            response = requests.get(f"https://{hostname}:{port}", timeout=timeout, verify=True)
            print(f"{Fore.GREEN}[+] Valid SSL certificate{Style.RESET_ALL}")
        except requests.exceptions.SSLError as e:
            issue = f"SSL certificate error: {str(e)}"
            results["issues"].append(issue)
            print(f"{Fore.RED}[!] {issue}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        
        if results["issues"]:
            print(f"{Fore.RED}[!] Found {len(results['issues'])} SSL/TLS issues:{Style.RESET_ALL}\n")
            for issue in results["issues"]:
                print(f"{Fore.YELLOW}  - {issue}{Style.RESET_ALL}")
            print()
            return {
                "success": True,
                "message": f"Found {len(results['issues'])} issues",
                "results": results
            }
        else:
            print(f"{Fore.GREEN}[+] No major SSL/TLS issues detected{Style.RESET_ALL}\n")
            return {
                "success": True,
                "message": "No major issues found",
                "results": results
            }
