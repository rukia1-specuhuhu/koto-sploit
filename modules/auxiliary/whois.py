"""WHOIS lookup module"""

import whois
from colorama import Fore, Style
from modules.base import BaseModule

class WhoisLookup(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "WHOIS domain information lookup"
        self.module_type = "auxiliary"
        self.options = {
            "DOMAIN": "",
        }
        self.required_options = ["DOMAIN"]
    
    def run(self):
        domain = self.get_option("DOMAIN")
        
        print(f"{Fore.YELLOW}[*] Looking up WHOIS information for: {domain}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        try:
            w = whois.whois(domain)
            
            print(f"{Fore.GREEN}[+] WHOIS Information:{Style.RESET_ALL}\n")
            
            info = {
                "Domain Name": w.get('domain_name') if isinstance(w, dict) else getattr(w, 'domain_name', None),
                "Registrar": w.get('registrar') if isinstance(w, dict) else getattr(w, 'registrar', None),
                "Creation Date": w.get('creation_date') if isinstance(w, dict) else getattr(w, 'creation_date', None),
                "Expiration Date": w.get('expiration_date') if isinstance(w, dict) else getattr(w, 'expiration_date', None),
                "Updated Date": w.get('updated_date') if isinstance(w, dict) else getattr(w, 'updated_date', None),
                "Name Servers": w.get('name_servers') if isinstance(w, dict) else getattr(w, 'name_servers', None),
                "Status": w.get('status') if isinstance(w, dict) else getattr(w, 'status', None),
                "Emails": w.get('emails') if isinstance(w, dict) else getattr(w, 'emails', None),
                "Organization": w.get('org') if isinstance(w, dict) else getattr(w, 'org', None),
                "Country": w.get('country') if isinstance(w, dict) else getattr(w, 'country', None),
            }
            
            for key, value in info.items():
                if value:
                    if isinstance(value, list):
                        print(f"{Fore.CYAN}  {key}:{Style.RESET_ALL}")
                        for item in value:
                            print(f"{Fore.WHITE}    - {item}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.CYAN}  {key}: {Fore.WHITE}{value}{Style.RESET_ALL}")
            
            print()
            
            return {
                "success": True,
                "message": "WHOIS lookup completed",
                "data": info
            }
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}\n")
            return {
                "success": False,
                "message": f"Error: {e}"
            }
