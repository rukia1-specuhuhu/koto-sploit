"""Report generator for pentesting results"""

import json
from datetime import datetime
from colorama import Fore, Style

class Reporter:
    def __init__(self):
        self.results = []
        self.session_start = datetime.now()
    
    def add_result(self, module_name, result):
        self.results.append({
            "timestamp": datetime.now().isoformat(),
            "module": module_name,
            "result": result
        })
    
    def generate_report(self, filename=None):
        if not filename:
            filename = f"kotosploit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "session_start": self.session_start.isoformat(),
            "session_end": datetime.now().isoformat(),
            "results": self.results
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"{Fore.GREEN}[+] Report saved to: {filename}{Style.RESET_ALL}")
            return filename
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving report: {e}{Style.RESET_ALL}")
            return None
    
    def show_summary(self):
        print(f"\n{Fore.YELLOW}Session Summary{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"  Start: {self.session_start}")
        print(f"  Modules executed: {len(self.results)}")
        print()
