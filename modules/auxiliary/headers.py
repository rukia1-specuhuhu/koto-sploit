"""HTTP header analyzer module"""

import requests
from colorama import Fore, Style
from modules.base import BaseModule

class HeaderAnalyzer(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "HTTP security headers analyzer"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "TIMEOUT": "10",
        }
        self.required_options = ["URL"]
        
        self.security_headers = {
            "Strict-Transport-Security": "HSTS - Forces HTTPS connections",
            "Content-Security-Policy": "CSP - Prevents XSS and injection attacks",
            "X-Frame-Options": "Prevents clickjacking attacks",
            "X-Content-Type-Options": "Prevents MIME type sniffing",
            "X-XSS-Protection": "Legacy XSS protection (mostly deprecated)",
            "Referrer-Policy": "Controls referrer information",
            "Permissions-Policy": "Controls browser features",
        }
    
    def run(self):
        url = self.get_option("URL")
        timeout = int(self.get_option("TIMEOUT"))
        
        print(f"{Fore.YELLOW}[*] Analyzing headers for: {url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            
            print(f"{Fore.GREEN}[+] All Response Headers:{Style.RESET_ALL}\n")
            for header, value in response.headers.items():
                print(f"{Fore.CYAN}  {header}: {Fore.WHITE}{value}{Style.RESET_ALL}")
            
            print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Security Headers Analysis:{Style.RESET_ALL}\n")
            
            missing_headers = []
            present_headers = []
            
            for header, description in self.security_headers.items():
                if header in response.headers:
                    print(f"{Fore.GREEN}[+] PRESENT: {header}{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}    {description}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}    Value: {response.headers[header]}{Style.RESET_ALL}\n")
                    present_headers.append(header)
                else:
                    print(f"{Fore.RED}[!] MISSING: {header}{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}    {description}{Style.RESET_ALL}\n")
                    missing_headers.append(header)
            
            print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            
            if missing_headers:
                print(f"{Fore.RED}[!] Missing {len(missing_headers)} security headers{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}[*] Consider implementing these headers to improve security{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.GREEN}[+] All recommended security headers are present!{Style.RESET_ALL}\n")
            
            return {
                "success": True,
                "message": f"Found {len(present_headers)}/{len(self.security_headers)} security headers",
                "present": present_headers,
                "missing": missing_headers,
                "all_headers": dict(response.headers)
            }
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}\n")
            return {
                "success": False,
                "message": f"Error: {e}"
            }
