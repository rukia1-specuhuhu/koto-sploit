"""Session management for Kotosploit"""

import pickle
import os
from datetime import datetime
from typing import Dict, Any, Optional
from colorama import Fore, Style

class SessionManager:
    def __init__(self, session_dir: str = "./sessions"):
        self.session_dir = session_dir
        self.current_session = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "targets": [],
            "modules_used": [],
            "options": {},
            "results": [],
            "notes": []
        }
        
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
    
    def save_session(self, session_name: str = None) -> str:
        if not session_name:
            session_name = f"session_{self.current_session['id']}.kts"
        
        filepath = os.path.join(self.session_dir, session_name)
        
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(self.current_session, f)
            print(f"{Fore.GREEN}[+] Session saved: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving session: {e}{Style.RESET_ALL}")
            return None
    
    def load_session(self, session_name: str) -> bool:
        filepath = os.path.join(self.session_dir, session_name)
        
        if not os.path.exists(filepath):
            print(f"{Fore.RED}[!] Session file not found: {filepath}{Style.RESET_ALL}")
            return False
        
        try:
            with open(filepath, 'rb') as f:
                self.current_session = pickle.load(f)
            print(f"{Fore.GREEN}[+] Session loaded: {filepath}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error loading session: {e}{Style.RESET_ALL}")
            return False
    
    def list_sessions(self):
        sessions = []
        for filename in os.listdir(self.session_dir):
            if filename.endswith('.kts'):
                filepath = os.path.join(self.session_dir, filename)
                sessions.append({
                    "name": filename,
                    "path": filepath,
                    "size": os.path.getsize(filepath),
                    "modified": datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                })
        return sessions
    
    def add_target(self, target: str):
        if target not in self.current_session["targets"]:
            self.current_session["targets"].append(target)
    
    def add_module_usage(self, module: str, options: Dict[str, Any]):
        self.current_session["modules_used"].append({
            "module": module,
            "options": options,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_result(self, module: str, result: Dict[str, Any]):
        self.current_session["results"].append({
            "module": module,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_note(self, note: str):
        self.current_session["notes"].append({
            "note": note,
            "timestamp": datetime.now().isoformat()
        })
    
    def set_option(self, key: str, value: Any):
        self.current_session["options"][key] = value
    
    def get_option(self, key: str, default: Any = None) -> Any:
        return self.current_session["options"].get(key, default)
    
    def clear_session(self):
        self.current_session = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "targets": [],
            "modules_used": [],
            "options": {},
            "results": [],
            "notes": []
        }
        print(f"{Fore.GREEN}[+] Session cleared{Style.RESET_ALL}")
    
    def show_session_info(self):
        print(f"\n{Fore.YELLOW}Current Session Information{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Session ID: {self.current_session['id']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Start Time: {self.current_session['start_time']}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Targets: {len(self.current_session['targets'])}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Modules Used: {len(self.current_session['modules_used'])}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Results Recorded: {len(self.current_session['results'])}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Notes: {len(self.current_session['notes'])}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
