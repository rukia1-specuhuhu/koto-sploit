"""Subdomain enumeration module"""

import dns.resolver
from colorama import Fore, Style
from modules.base import BaseModule

class SubdomainEnumerator(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Subdomain enumeration via DNS queries"
        self.module_type = "auxiliary"
        self.options = {
            "DOMAIN": "",
            "WORDLIST": "default",
        }
        self.required_options = ["DOMAIN"]
        
        self.default_wordlist = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp",
            "pop", "ns1", "webdisk", "ns2", "cpanel", "whm",
            "autodiscover", "autoconfig", "m", "imap", "test",
            "ns", "blog", "pop3", "dev", "www2", "admin",
            "forum", "news", "vpn", "ns3", "mail2", "new",
            "mysql", "old", "lists", "support", "mobile", "mx",
            "static", "docs", "beta", "shop", "sql", "secure",
            "demo", "cp", "calendar", "wiki", "web", "media",
            "email", "images", "img", "www1", "intranet", "portal",
            "video", "sip", "dns2", "api", "cdn", "stats",
            "dns1", "ns4", "www3", "dns", "search", "staging",
        ]
    
    def run(self):
        domain = self.get_option("DOMAIN")
        wordlist_type = self.get_option("WORDLIST")
        
        print(f"{Fore.YELLOW}[*] Target domain: {domain}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Wordlist: {wordlist_type}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        found = []
        wordlist = self.default_wordlist
        
        for i, subdomain in enumerate(wordlist, 1):
            full_domain = f"{subdomain}.{domain}"
            print(f"{Fore.CYAN}[{i}/{len(wordlist)}] Testing: {full_domain}{Style.RESET_ALL}", end='\r')
            
            try:
                answers = dns.resolver.resolve(full_domain, 'A')
                ips = [str(rdata) for rdata in answers]
                found.append((full_domain, ips))
                print(f"{Fore.GREEN}[+] FOUND: {full_domain} -> {', '.join(ips)}{Style.RESET_ALL}")
            except Exception:
                pass
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        
        if found:
            print(f"{Fore.GREEN}[+] Found {len(found)} subdomains:{Style.RESET_ALL}\n")
            for subdomain, ips in found:
                print(f"{Fore.CYAN}  {subdomain} -> {', '.join(ips)}{Style.RESET_ALL}")
            
            return {
                "success": True,
                "message": f"Found {len(found)} subdomains",
                "found": found
            }
        else:
            print(f"{Fore.YELLOW}[*] No subdomains found{Style.RESET_ALL}\n")
            return {
                "success": True,
                "message": "No subdomains found"
            }
