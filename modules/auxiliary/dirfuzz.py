"""Directory and file fuzzing module"""

import requests
from colorama import Fore, Style
from modules.base import BaseModule

class DirectoryFuzzer(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Directory and file fuzzing tool"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "WORDLIST": "default",
            "EXTENSIONS": "",
            "TIMEOUT": "5",
            "THREADS": "10",
        }
        self.required_options = ["URL"]
        
        self.default_wordlist = [
            "admin", "login", "dashboard", "config", "backup", "test",
            "api", "uploads", "images", "css", "js", "assets",
            "wp-admin", "phpmyadmin", "cpanel", "cgi-bin",
            "temp", "tmp", "old", "new", "debug", "dev",
            "staging", "production", "database", "db", "sql",
            ".git", ".env", ".htaccess", "robots.txt", "sitemap.xml",
            "readme", "README", "LICENSE", "install", "setup",
        ]
    
    def run(self):
        url = self.get_option("URL").rstrip('/')
        wordlist_type = self.get_option("WORDLIST")
        extensions = self.get_option("EXTENSIONS").split(',') if self.get_option("EXTENSIONS") else ['']
        timeout = int(self.get_option("TIMEOUT"))
        
        print(f"{Fore.YELLOW}[*] Target URL: {url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Wordlist: {wordlist_type}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        found = []
        wordlist = self.default_wordlist
        
        total = len(wordlist) * len(extensions) if extensions else len(wordlist)
        current = 0
        
        for word in wordlist:
            for ext in extensions:
                current += 1
                path = f"{word}{ext}"
                test_url = f"{url}/{path}"
                
                print(f"{Fore.CYAN}[{current}/{total}] Testing: /{path}{Style.RESET_ALL}", end='\r')
                
                try:
                    response = requests.get(test_url, timeout=timeout, verify=False, allow_redirects=False)
                    
                    if response.status_code == 200:
                        found.append((path, response.status_code, len(response.content)))
                        print(f"{Fore.GREEN}[+] FOUND: /{path} (Status: {response.status_code}, Size: {len(response.content)} bytes){Style.RESET_ALL}")
                    elif response.status_code in [301, 302, 307, 308]:
                        found.append((path, response.status_code, 0))
                        print(f"{Fore.YELLOW}[*] REDIRECT: /{path} (Status: {response.status_code}){Style.RESET_ALL}")
                    elif response.status_code == 403:
                        found.append((path, response.status_code, 0))
                        print(f"{Fore.MAGENTA}[!] FORBIDDEN: /{path} (Status: {response.status_code}){Style.RESET_ALL}")
                        
                except Exception:
                    pass
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        
        if found:
            print(f"{Fore.GREEN}[+] Found {len(found)} accessible paths:{Style.RESET_ALL}\n")
            for path, status, size in found:
                print(f"{Fore.CYAN}  /{path} - Status: {status}, Size: {size} bytes{Style.RESET_ALL}")
            
            return {
                "success": True,
                "message": f"Found {len(found)} paths",
                "found": found
            }
        else:
            print(f"{Fore.YELLOW}[*] No accessible paths found{Style.RESET_ALL}\n")
            return {
                "success": True,
                "message": "No paths found"
            }
