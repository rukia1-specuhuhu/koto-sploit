"""CMS (Content Management System) detection module"""

import requests
import re
from colorama import Fore, Style
from modules.base import BaseModule

class CMSDetector(BaseModule):
    def __init__(self):
        super().__init__()
        self.description = "Detect and fingerprint CMS platforms"
        self.module_type = "auxiliary"
        self.options = {
            "URL": "",
            "TIMEOUT": "10",
        }
        self.required_options = ["URL"]
        
        self.cms_signatures = {
            "WordPress": [
                ("/wp-content/", "Path"),
                ("/wp-includes/", "Path"),
                ("/wp-admin/", "Path"),
                ("wp-content", "HTML"),
                ("wp-includes", "HTML"),
                ('<meta name="generator" content="WordPress', "Meta"),
            ],
            "Joomla": [
                ("/administrator/", "Path"),
                ("/components/", "Path"),
                ("/modules/", "Path"),
                ("Joomla!", "HTML"),
                ('<meta name="generator" content="Joomla', "Meta"),
                ("/media/system/js/", "Path"),
            ],
            "Drupal": [
                ("/sites/default/", "Path"),
                ("/sites/all/", "Path"),
                ("/misc/drupal.js", "Path"),
                ("Drupal", "HTML"),
                ('<meta name="generator" content="Drupal', "Meta"),
                ("/core/misc/drupal.js", "Path"),
            ],
            "Magento": [
                ("/skin/frontend/", "Path"),
                ("/js/mage/", "Path"),
                ("Mage.Cookies", "HTML"),
                ("Magento", "HTML"),
                ("/media/wysiwyg/", "Path"),
            ],
            "PrestaShop": [
                ("/modules/", "Path"),
                ("/themes/", "Path"),
                ("prestashop", "HTML"),
                ("/js/tools.js", "Path"),
            ],
            "OpenCart": [
                ("/catalog/view/", "Path"),
                ("catalog/view/theme", "HTML"),
                ("index.php?route=", "HTML"),
            ],
            "Shopify": [
                ("cdn.shopify.com", "HTML"),
                ("myshopify.com", "HTML"),
                ("Shopify.theme", "HTML"),
            ],
            "Wix": [
                ("wix.com", "HTML"),
                ("_wix", "HTML"),
                ("X-Wix-", "Header"),
            ],
            "Squarespace": [
                ("squarespace.com", "HTML"),
                ("squarespace-cdn.com", "HTML"),
                ("X-Sqsp-", "Header"),
            ],
            "Ghost": [
                ("/ghost/", "Path"),
                ("ghost.min.js", "HTML"),
                ('<meta name="generator" content="Ghost', "Meta"),
            ],
            "Typo3": [
                ("/typo3/", "Path"),
                ("typo3", "HTML"),
                ("TYPO3", "HTML"),
            ],
            "DotNetNuke": [
                ("/Portals/", "Path"),
                ("DotNetNuke", "HTML"),
                ("DNN Platform", "HTML"),
            ],
            "MediaWiki": [
                ("/index.php?title=", "Path"),
                ("MediaWiki", "HTML"),
                ("wgAction", "HTML"),
            ],
        }
        
        self.version_patterns = {
            "WordPress": [
                (r'<meta name="generator" content="WordPress ([\d.]+)"', "Meta Tag"),
                (r'/wp-includes/js/wp-embed\.min\.js\?ver=([\d.]+)', "Script Version"),
            ],
            "Joomla": [
                (r'<meta name="generator" content="Joomla! ([\d.]+)"', "Meta Tag"),
            ],
            "Drupal": [
                (r'<meta name="generator" content="Drupal ([\d.]+)"', "Meta Tag"),
                (r'Drupal ([\d.]+)', "HTML"),
            ],
        }
    
    def run(self):
        url = self.get_option("URL")
        timeout = int(self.get_option("TIMEOUT"))
        
        print(f"{Fore.YELLOW}[*] Detecting CMS for: {url}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
        
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            html = response.text
            headers = response.headers
            
            detected_cms = []
            
            for cms_name, signatures in self.cms_signatures.items():
                matches = []
                
                for signature, sig_type in signatures:
                    if sig_type == "Path":
                        test_url = url.rstrip('/') + signature
                        try:
                            test_response = requests.get(test_url, timeout=5, verify=False)
                            if test_response.status_code in [200, 301, 302, 403]:
                                matches.append(f"{sig_type}: {signature}")
                        except Exception:
                            pass
                    
                    elif sig_type == "HTML" and signature in html:
                        matches.append(f"{sig_type}: {signature}")
                    
                    elif sig_type == "Meta" and signature in html:
                        matches.append(f"{sig_type}: Found")
                    
                    elif sig_type == "Header":
                        for header_name, header_value in headers.items():
                            if signature.lower() in header_name.lower():
                                matches.append(f"{sig_type}: {header_name}")
                
                if matches:
                    version = self._detect_version(cms_name, html)
                    detected_cms.append({
                        "name": cms_name,
                        "version": version,
                        "confidence": len(matches) * 20,
                        "matches": matches
                    })
            
            print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
            
            if detected_cms:
                detected_cms.sort(key=lambda x: x['confidence'], reverse=True)
                
                print(f"{Fore.GREEN}[+] Detected CMS platforms:{Style.RESET_ALL}\n")
                for cms in detected_cms:
                    confidence = min(cms['confidence'], 100)
                    print(f"{Fore.CYAN}  {cms['name']}{Style.RESET_ALL}")
                    if cms['version']:
                        print(f"{Fore.YELLOW}    Version: {cms['version']}{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}    Confidence: {confidence}%{Style.RESET_ALL}")
                    print(f"{Fore.WHITE}    Evidence: {', '.join(cms['matches'][:3])}{Style.RESET_ALL}\n")
                
                return {
                    "success": True,
                    "message": f"Detected {len(detected_cms)} CMS platform(s)",
                    "cms": detected_cms
                }
            else:
                print(f"{Fore.YELLOW}[*] No known CMS detected{Style.RESET_ALL}\n")
                return {
                    "success": True,
                    "message": "No CMS detected"
                }
        
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}\n")
            return {
                "success": False,
                "message": f"Error: {e}"
            }
    
    def _detect_version(self, cms_name: str, html: str) -> str:
        if cms_name not in self.version_patterns:
            return "Unknown"
        
        for pattern, source in self.version_patterns[cms_name]:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return "Unknown"
