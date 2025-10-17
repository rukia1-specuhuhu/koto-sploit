"""Information disclosure scanner module"""

import requests
from colorama import Fore, Style
from modules.base import BaseModule

class InformationDisclosure(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Scan for information disclosure vulnerabilities"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "TIMEOUT": "10",
        }
        self.required_options = ["URL"]
        
        self.sensitive_paths = [
            ".git/config",
            ".git/HEAD",
            ".svn/entries",
            ".env",
            ".DS_Store",
            "web.config",
            "app.config",
            "config.php",
            "config.json",
            "configuration.php",
            "settings.php",
            "settings.json",
            "database.yml",
            "database.php",
            "db_config.php",
            "wp-config.php",
            "wp-config.php.bak",
            "admin/config.php",
            "includes/config.php",
            "application/config/database.php",
            "backup.sql",
            "dump.sql",
            "database.sql",
            "phpinfo.php",
            "info.php",
            "test.php",
            "debug.log",
            "error.log",
            "error_log",
            "access.log",
            "access_log",
            ".htaccess",
            ".htpasswd",
            "crossdomain.xml",
            "clientaccesspolicy.xml",
            "composer.json",
            "composer.lock",
            "package.json",
            "package-lock.json",
            "yarn.lock",
            "Gemfile",
            "Gemfile.lock",
            "requirements.txt",
            "Pipfile",
            "README.md",
            "CHANGELOG.md",
            "LICENSE",
        ]
        
        self.sensitive_patterns = [
            (r'password\s*=\s*[\'"]([^\'"]+)[\'"]', 'Password in config'),
            (r'api[_-]?key\s*=\s*[\'"]([^\'"]+)[\'"]', 'API Key'),
            (r'secret[_-]?key\s*=\s*[\'"]([^\'"]+)[\'"]', 'Secret Key'),
            (r'access[_-]?token\s*=\s*[\'"]([^\'"]+)[\'"]', 'Access Token'),
            (r'mysql://([^@]+)@', 'MySQL Credentials'),
            (r'postgresql://([^@]+)@', 'PostgreSQL Credentials'),
            (r'mongodb://([^@]+)@', 'MongoDB Credentials'),
            (r'-----BEGIN.*PRIVATE KEY-----', 'Private Key'),
            (r'-----BEGIN RSA PRIVATE KEY-----', 'RSA Private Key'),
            (r'AWS[_-]?SECRET[_-]?ACCESS[_-]?KEY', 'AWS Secret Key'),
            (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
        ]
    
    def run(self):
        url = self.get_option("URL").rstrip('/')
        timeout = int(self.get_option("TIMEOUT"))
        
        print(f"{Fore.YELLOW}[*] Scanning for information disclosure: {url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        disclosed_info = []
        
        print(f"{Fore.CYAN}[*] Checking sensitive files...{Style.RESET_ALL}\n")
        
        for path in self.sensitive_paths:
            test_url = f"{url}/{path}"
            print(f"{Fore.CYAN}Testing: {path}{Style.RESET_ALL}", end='\r')
            
            try:
                response = requests.get(test_url, timeout=timeout, verify=False)
                
                if response.status_code == 200:
                    disclosed_info.append({
                        "type": "Sensitive File",
                        "path": path,
                        "url": test_url,
                        "size": len(response.content)
                    })
                    print(f"{Fore.RED}[!] FOUND: {path} (Size: {len(response.content)} bytes){Style.RESET_ALL}")
                    
                    for pattern, description in self.sensitive_patterns:
                        import re
                        if re.search(pattern, response.text, re.IGNORECASE):
                            disclosed_info.append({
                                "type": "Sensitive Data",
                                "path": path,
                                "url": test_url,
                                "description": description
                            })
                            print(f"{Fore.RED}    [!] Contains: {description}{Style.RESET_ALL}")
            
            except Exception:
                pass
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        
        if disclosed_info:
            print(f"{Fore.RED}[!] Found {len(disclosed_info)} information disclosure issues:{Style.RESET_ALL}\n")
            for info in disclosed_info:
                print(f"{Fore.YELLOW}  Type: {info['type']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  Path: {info['path']}{Style.RESET_ALL}")
                if 'description' in info:
                    print(f"{Fore.RED}  Description: {info['description']}{Style.RESET_ALL}")
                print()
            
            return {
                "success": True,
                "message": f"Found {len(disclosed_info)} disclosure issues",
                "disclosed": disclosed_info
            }
        else:
            print(f"{Fore.GREEN}[+] No obvious information disclosure issues found{Style.RESET_ALL}\n")
            return {
                "success": True,
                "message": "No issues found"
            }
