"""Technology stack detection module"""

import requests
import re
from colorama import Fore, Style
from modules.base import BaseModule

class TechStackDetector(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Detect web technologies and frameworks"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "TIMEOUT": "10",
        }
        self.required_options = ["URL"]
        
        self.tech_signatures = {
            "Frontend Frameworks": {
                "React": ["react", "_reactRootContainer", "data-reactroot", "react-dom"],
                "Angular": ["ng-version", "angular", "_ngcontent", "ng-app"],
                "Vue.js": ["vue", "__vue__", "v-cloak", "data-v-"],
                "jQuery": ["jquery", "jQuery"],
                "Bootstrap": ["bootstrap", "btn btn-", "col-md-"],
                "Tailwind CSS": ["tailwindcss", "tw-"],
            },
            "Backend Technologies": {
                "PHP": [".php", "<?php", "PHPSESSID"],
                "ASP.NET": [".aspx", "ASP.NET", "__VIEWSTATE"],
                "Java": [".jsp", ".do", "jsessionid"],
                "Python": ["django", "flask", "wsgi"],
                "Ruby": ["ruby", "rails", "_rails_session"],
                "Node.js": ["express", "koa", "next.js"],
            },
            "Web Servers": {
                "Apache": ["Apache", "mod_"],
                "Nginx": ["nginx"],
                "IIS": ["IIS", "Microsoft-IIS"],
                "LiteSpeed": ["LiteSpeed"],
                "Cloudflare": ["cloudflare", "cf-ray"],
            },
            "CDNs": {
                "Cloudflare": ["cloudflare-cdn", "cf-cache"],
                "Akamai": ["akamai"],
                "Amazon CloudFront": ["cloudfront.net"],
                "Fastly": ["fastly"],
            },
            "Analytics": {
                "Google Analytics": ["google-analytics", "ga.js", "gtag"],
                "Facebook Pixel": ["facebook.net/tr", "fbq"],
                "Hotjar": ["hotjar"],
                "Mixpanel": ["mixpanel"],
            },
            "JavaScript Libraries": {
                "Lodash": ["lodash", "_."],
                "Moment.js": ["moment.js"],
                "D3.js": ["d3.js", "d3.min.js"],
                "Chart.js": ["chart.js"],
                "Three.js": ["three.js"],
            },
        }
        
        self.header_signatures = {
            "Server": ["Apache", "nginx", "IIS", "LiteSpeed", "Cloudflare"],
            "X-Powered-By": ["PHP", "ASP.NET", "Express", "Django"],
            "X-Generator": ["Drupal", "WordPress", "Joomla"],
            "X-Framework": ["Laravel", "CodeIgniter", "Symfony"],
        }
    
    def run(self):
        url = self.get_option("URL")
        timeout = int(self.get_option("TIMEOUT"))
        
        print(f"{Fore.YELLOW}[*] Detecting technology stack for: {url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            html = response.text.lower()
            headers = response.headers
            
            detected_tech = {}
            
            print(f"{Fore.CYAN}[*] Analyzing HTML and headers...{Style.RESET_ALL}\n")
            
            for category, technologies in self.tech_signatures.items():
                detected_tech[category] = []
                
                for tech_name, signatures in technologies.items():
                    for signature in signatures:
                        if signature.lower() in html:
                            if tech_name not in detected_tech[category]:
                                detected_tech[category].append(tech_name)
                                print(f"{Fore.GREEN}[+] Found: {tech_name} ({category}){Style.RESET_ALL}")
                            break
            
            print(f"\n{Fore.CYAN}[*] Analyzing HTTP headers...{Style.RESET_ALL}\n")
            
            header_tech = []
            for header_name, possible_values in self.header_signatures.items():
                if header_name in headers:
                    header_value = headers[header_name]
                    header_tech.append(f"{header_name}: {header_value}")
                    print(f"{Fore.GREEN}[+] Header: {header_name} = {header_value}{Style.RESET_ALL}")
                    
                    for value in possible_values:
                        if value.lower() in header_value.lower():
                            for category in detected_tech:
                                if value not in detected_tech[category]:
                                    detected_tech[category].append(value)
            
            cookies = response.cookies
            if cookies:
                print(f"\n{Fore.CYAN}[*] Cookies detected:{Style.RESET_ALL}")
                for cookie in cookies:
                    print(f"{Fore.YELLOW}  {cookie.name} = {cookie.value[:50]}...{Style.RESET_ALL}")
            
            print(f"\n{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Technology Stack Summary:{Style.RESET_ALL}\n")
            
            total_detected = 0
            for category, techs in detected_tech.items():
                if techs:
                    print(f"{Fore.CYAN}{category}:{Style.RESET_ALL}")
                    for tech in techs:
                        print(f"{Fore.WHITE}  - {tech}{Style.RESET_ALL}")
                        total_detected += 1
                    print()
            
            if total_detected == 0:
                print(f"{Fore.YELLOW}[*] No specific technologies detected{Style.RESET_ALL}\n")
            
            return {
                "success": True,
                "message": f"Detected {total_detected} technologies",
                "technologies": detected_tech,
                "headers": dict(headers),
                "header_tech": header_tech
            }
        
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}\n")
            return {
                "success": False,
                "message": f"Error: {e}"
            }
