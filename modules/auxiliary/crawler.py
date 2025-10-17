"""Web crawler module for discovering endpoints"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style
from modules.base import BaseModule

class WebCrawler(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Web crawler for discovering endpoints and forms"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "DEPTH": "2",
            "TIMEOUT": "10",
        }
        self.required_options = ["URL"]
        self.visited_urls = set()
        self.discovered_urls = set()
        self.forms = []
    
    def run(self):
        url = self.get_option("URL")
        depth = int(self.get_option("DEPTH"))
        timeout = int(self.get_option("TIMEOUT"))
        
        print(f"{Fore.YELLOW}[*] Starting web crawler on: {url}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Max depth: {depth}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        self._crawl(url, depth, timeout)
        
        print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Crawl complete!{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}Discovered URLs: {len(self.discovered_urls)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Discovered Forms: {len(self.forms)}{Style.RESET_ALL}\n")
        
        if self.discovered_urls:
            print(f"{Fore.YELLOW}URLs:{Style.RESET_ALL}")
            for discovered_url in list(self.discovered_urls)[:20]:
                print(f"{Fore.WHITE}  - {discovered_url}{Style.RESET_ALL}")
            if len(self.discovered_urls) > 20:
                print(f"{Fore.CYAN}  ... and {len(self.discovered_urls) - 20} more{Style.RESET_ALL}")
        
        if self.forms:
            print(f"\n{Fore.YELLOW}Forms:{Style.RESET_ALL}")
            for i, form in enumerate(self.forms[:10], 1):
                print(f"{Fore.WHITE}  {i}. {form['action']} ({form['method']}){Style.RESET_ALL}")
            if len(self.forms) > 10:
                print(f"{Fore.CYAN}  ... and {len(self.forms) - 10} more{Style.RESET_ALL}")
        
        print()
        
        return {
            "success": True,
            "message": f"Found {len(self.discovered_urls)} URLs and {len(self.forms)} forms",
            "urls": list(self.discovered_urls),
            "forms": self.forms
        }
    
    def _crawl(self, url: str, depth: int, timeout: int, current_depth: int = 0):
        if current_depth > depth or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                
                if urlparse(absolute_url).netloc == urlparse(url).netloc:
                    self.discovered_urls.add(absolute_url)
                    print(f"{Fore.CYAN}[+] Found: {absolute_url}{Style.RESET_ALL}")
                    
                    if current_depth < depth:
                        self._crawl(absolute_url, depth, timeout, current_depth + 1)
            
            for form in soup.find_all('form'):
                action = form.get('action', '')
                method = form.get('method', 'get').upper()
                absolute_action = urljoin(url, action)
                
                form_data = {
                    "url": url,
                    "action": absolute_action,
                    "method": method,
                    "inputs": []
                }
                
                for input_tag in form.find_all('input'):
                    form_data["inputs"].append({
                        "name": input_tag.get('name', ''),
                        "type": input_tag.get('type', 'text')
                    })
                
                self.forms.append(form_data)
                print(f"{Fore.GREEN}[+] Found form: {absolute_action} ({method}){Style.RESET_ALL}")
        
        except Exception:
            pass
