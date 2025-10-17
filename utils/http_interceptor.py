"""HTTP request/response interceptor and modifier"""

import requests
from typing import Dict, Any, Optional, Callable
from colorama import Fore, Style

class HTTPInterceptor:
    def __init__(self):
        self.request_hooks = []
        self.response_hooks = []
        self.default_headers = {
            'User-Agent': 'Kotosploit/1.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.proxy_config = None
        self.auth_config = None
    
    def add_request_hook(self, hook: Callable):
        self.request_hooks.append(hook)
    
    def add_response_hook(self, hook: Callable):
        self.response_hooks.append(hook)
    
    def set_default_header(self, key: str, value: str):
        self.default_headers[key] = value
    
    def remove_default_header(self, key: str):
        if key in self.default_headers:
            del self.default_headers[key]
    
    def set_proxy(self, proxy_url: str):
        self.proxy_config = {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def set_auth(self, username: str, password: str):
        self.auth_config = (username, password)
    
    def send_request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        headers = self.default_headers.copy()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers
        
        if self.proxy_config and 'proxies' not in kwargs:
            kwargs['proxies'] = self.proxy_config
        
        if self.auth_config and 'auth' not in kwargs:
            kwargs['auth'] = self.auth_config
        
        kwargs.setdefault('verify', False)
        kwargs.setdefault('timeout', 10)
        
        for hook in self.request_hooks:
            method, url, kwargs = hook(method, url, kwargs)
        
        try:
            response = requests.request(method, url, **kwargs)
            
            for hook in self.response_hooks:
                response = hook(response)
            
            return response
        except Exception as e:
            print(f"{Fore.RED}[!] Request failed: {e}{Style.RESET_ALL}")
            return None
    
    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.send_request('GET', url, **kwargs)
    
    def post(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.send_request('POST', url, **kwargs)
    
    def put(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.send_request('PUT', url, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.send_request('DELETE', url, **kwargs)
    
    def options(self, url: str, **kwargs) -> Optional[requests.Response]:
        return self.send_request('OPTIONS', url, **kwargs)
    
    def log_request(self, method: str, url: str, kwargs: Dict[str, Any]):
        print(f"{Fore.CYAN}[→] {method} {url}{Style.RESET_ALL}")
        if kwargs.get('headers'):
            print(f"{Fore.YELLOW}    Headers: {kwargs['headers']}{Style.RESET_ALL}")
        if kwargs.get('data'):
            print(f"{Fore.YELLOW}    Data: {kwargs['data']}{Style.RESET_ALL}")
        return method, url, kwargs
    
    def log_response(self, response: requests.Response):
        status_color = Fore.GREEN if response.status_code < 400 else Fore.RED
        print(f"{status_color}[←] {response.status_code} {response.reason}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Size: {len(response.content)} bytes{Style.RESET_ALL}")
        return response
    
    def inject_header(self, header_name: str, header_value: str):
        def hook(method, url, kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers'][header_name] = header_value
            return method, url, kwargs
        self.add_request_hook(hook)
    
    def modify_user_agent(self, user_agent: str):
        self.set_default_header('User-Agent', user_agent)
    
    def enable_debug_logging(self):
        self.add_request_hook(self.log_request)
        self.add_response_hook(self.log_response)
