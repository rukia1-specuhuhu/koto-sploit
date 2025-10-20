import pickle
import os
import json
import sqlite3
import shutil
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from colorama import Fore, Style
import hashlib
import threading
import time

class SessionManager:
    def __init__(self, session_dir: str = "./sessions", use_database: bool = True):
        self.session_dir = session_dir
        self.use_database = use_database
        self.current_session = {
            "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "targets": [],
            "modules_used": [],
            "options": {},
            "results": [],
            "notes": [],
            "tags": [],
            "metadata": {}
        }
        
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        
        if use_database:
            self._init_database()
        
        self._auto_save_thread = None
        self._stop_auto_save = False
        self._last_save_time = datetime.now()
    
    def _init_database(self):
        db_path = os.path.join(self.session_dir, "sessions.db")
        self.db_conn = sqlite3.connect(db_path)
        self.db_cursor = self.db_conn.cursor()
        
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            name TEXT,
            start_time TEXT,
            end_time TEXT,
            data TEXT,
            tags TEXT,
            metadata TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        ''')
        
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            target TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
        ''')
        
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            module TEXT,
            options TEXT,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
        ''')
        
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            module TEXT,
            result TEXT,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
        ''')
        
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            note TEXT,
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
        ''')
        
        self.db_conn.commit()
    
    def start_auto_save(self, interval_seconds: int = 60):
        if self._auto_save_thread and self._auto_save_thread.is_alive():
            print(f"{Fore.YELLOW}[!] Auto-save is already running{Style.RESET_ALL}")
            return
        
        self._stop_auto_save = False
        self._auto_save_thread = threading.Thread(target=self._auto_save_worker, args=(interval_seconds,))
        self._auto_save_thread.daemon = True
        self._auto_save_thread.start()
        print(f"{Fore.GREEN}[+] Auto-save started with {interval_seconds}s interval{Style.RESET_ALL}")
    
    def stop_auto_save(self):
        if not self._auto_save_thread or not self._auto_save_thread.is_alive():
            print(f"{Fore.YELLOW}[!] Auto-save is not running{Style.RESET_ALL}")
            return
        
        self._stop_auto_save = True
        self._auto_save_thread.join()
        print(f"{Fore.GREEN}[+] Auto-save stopped{Style.RESET_ALL}")
    
    def _auto_save_worker(self, interval_seconds: int):
        while not self._stop_auto_save:
            time.sleep(interval_seconds)
            if not self._stop_auto_save and (datetime.now() - self._last_save_time).seconds >= interval_seconds:
                self.save_session(f"autosave_{self.current_session['id']}.kts")
                self._last_save_time = datetime.now()
    
    def save_session(self, session_name: str = None, format: str = "pickle") -> str:
        if not session_name:
            session_name = f"session_{self.current_session['id']}.kts"
        
        filepath = os.path.join(self.session_dir, session_name)
        
        try:
            if format.lower() == "json":
                with open(filepath, 'w') as f:
                    json.dump(self.current_session, f, indent=2)
            elif format.lower() == "pickle":
                with open(filepath, 'wb') as f:
                    pickle.dump(self.current_session, f)
            else:
                print(f"{Fore.RED}[!] Unsupported format: {format}{Style.RESET_ALL}")
                return None
            
            if self.use_database:
                self._save_to_database(session_name.replace('.kts', ''))
            
            print(f"{Fore.GREEN}[+] Session saved: {filepath}{Style.RESET_ALL}")
            return filepath
        except Exception as e:
            print(f"{Fore.RED}[!] Error saving session: {e}{Style.RESET_ALL}")
            return None
    
    def _save_to_database(self, session_name: str):
        session_id = self.current_session['id']
        start_time = self.current_session['start_time']
        end_time = datetime.now().isoformat()
        data = json.dumps(self.current_session)
        tags = json.dumps(self.current_session.get('tags', []))
        metadata = json.dumps(self.current_session.get('metadata', {}))
        created_at = datetime.now().isoformat()
        updated_at = datetime.now().isoformat()
        
        self.db_cursor.execute('''
        INSERT OR REPLACE INTO sessions 
        (id, name, start_time, end_time, data, tags, metadata, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (session_id, session_name, start_time, end_time, data, tags, metadata, created_at, updated_at))
        
        self.db_cursor.execute('DELETE FROM session_targets WHERE session_id = ?', (session_id,))
        for target in self.current_session.get('targets', []):
            self.db_cursor.execute('INSERT INTO session_targets (session_id, target) VALUES (?, ?)', 
                                 (session_id, target))
        
        self.db_cursor.execute('DELETE FROM session_modules WHERE session_id = ?', (session_id,))
        for module_usage in self.current_session.get('modules_used', []):
            module = module_usage.get('module', '')
            options = json.dumps(module_usage.get('options', {}))
            timestamp = module_usage.get('timestamp', datetime.now().isoformat())
            self.db_cursor.execute('INSERT INTO session_modules (session_id, module, options, timestamp) VALUES (?, ?, ?, ?)', 
                                 (session_id, module, options, timestamp))
        
        self.db_cursor.execute('DELETE FROM session_results WHERE session_id = ?', (session_id,))
        for result in self.current_session.get('results', []):
            module = result.get('module', '')
            result_data = json.dumps(result.get('result', {}))
            timestamp = result.get('timestamp', datetime.now().isoformat())
            self.db_cursor.execute('INSERT INTO session_results (session_id, module, result, timestamp) VALUES (?, ?, ?, ?)', 
                                 (session_id, module, result_data, timestamp))
        
        self.db_cursor.execute('DELETE FROM session_notes WHERE session_id = ?', (session_id,))
        for note in self.current_session.get('notes', []):
            note_text = note.get('note', '')
            timestamp = note.get('timestamp', datetime.now().isoformat())
            self.db_cursor.execute('INSERT INTO session_notes (session_id, note, timestamp) VALUES (?, ?, ?)', 
                                 (session_id, note_text, timestamp))
        
        self.db_conn.commit()
    
    def load_session(self, session_name: str, format: str = "pickle") -> bool:
        filepath = os.path.join(self.session_dir, session_name)
        
        if not os.path.exists(filepath):
            if self.use_database:
                return self._load_from_database(session_name.replace('.kts', ''))
            else:
                print(f"{Fore.RED}[!] Session file not found: {filepath}{Style.RESET_ALL}")
                return False
        
        try:
            if format.lower() == "json":
                with open(filepath, 'r') as f:
                    self.current_session = json.load(f)
            elif format.lower() == "pickle":
                with open(filepath, 'rb') as f:
                    self.current_session = pickle.load(f)
            else:
                print(f"{Fore.RED}[!] Unsupported format: {format}{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}[+] Session loaded: {filepath}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error loading session: {e}{Style.RESET_ALL}")
            return False
    
    def _load_from_database(self, session_id: str) -> bool:
        self.db_cursor.execute('SELECT data FROM sessions WHERE id = ?', (session_id,))
        result = self.db_cursor.fetchone()
        
        if not result:
            print(f"{Fore.RED}[!] Session not found in database: {session_id}{Style.RESET_ALL}")
            return False
        
        try:
            self.current_session = json.loads(result[0])
            print(f"{Fore.GREEN}[+] Session loaded from database: {session_id}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error loading session from database: {e}{Style.RESET_ALL}")
            return False
    
    def list_sessions(self, use_database: bool = None) -> List[Dict[str, Any]]:
        if use_database is None:
            use_database = self.use_database
        
        if use_database:
            return self._list_sessions_from_database()
        else:
            return self._list_sessions_from_files()
    
    def _list_sessions_from_files(self) -> List[Dict[str, Any]]:
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
    
    def _list_sessions_from_database(self) -> List[Dict[str, Any]]:
        sessions = []
        self.db_cursor.execute('SELECT id, name, start_time, end_time, tags, metadata, created_at, updated_at FROM sessions')
        
        for row in self.db_cursor.fetchall():
            session_id, name, start_time, end_time, tags, metadata, created_at, updated_at = row
            try:
                tags_data = json.loads(tags) if tags else []
                metadata_data = json.loads(metadata) if metadata else {}
            except:
                tags_data = []
                metadata_data = {}
            
            sessions.append({
                "id": session_id,
                "name": name,
                "start_time": start_time,
                "end_time": end_time,
                "tags": tags_data,
                "metadata": metadata_data,
                "created_at": created_at,
                "updated_at": updated_at
            })
        
        return sessions
    
    def delete_session(self, session_name: str, use_database: bool = None) -> bool:
        if use_database is None:
            use_database = self.use_database
        
        filepath = os.path.join(self.session_dir, session_name)
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            
            if use_database:
                session_id = session_name.replace('.kts', '')
                self.db_cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
                self.db_cursor.execute('DELETE FROM session_targets WHERE session_id = ?', (session_id,))
                self.db_cursor.execute('DELETE FROM session_modules WHERE session_id = ?', (session_id,))
                self.db_cursor.execute('DELETE FROM session_results WHERE session_id = ?', (session_id,))
                self.db_cursor.execute('DELETE FROM session_notes WHERE session_id = ?', (session_id,))
                self.db_conn.commit()
            
            print(f"{Fore.GREEN}[+] Session deleted: {session_name}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error deleting session: {e}{Style.RESET_ALL}")
            return False
    
    def export_session(self, session_name: str, export_path: str, format: str = "json") -> bool:
        if session_name.endswith('.kts'):
            session_id = session_name.replace('.kts', '')
        else:
            session_id = session_name
        
        if self.use_database:
            self.db_cursor.execute('SELECT data FROM sessions WHERE id = ?', (session_id,))
            result = self.db_cursor.fetchone()
            
            if not result:
                print(f"{Fore.RED}[!] Session not found: {session_name}{Style.RESET_ALL}")
                return False
            
            try:
                session_data = json.loads(result[0])
            except Exception as e:
                print(f"{Fore.RED}[!] Error parsing session data: {e}{Style.RESET_ALL}")
                return False
        else:
            filepath = os.path.join(self.session_dir, session_name)
            
            if not os.path.exists(filepath):
                print(f"{Fore.RED}[!] Session file not found: {filepath}{Style.RESET_ALL}")
                return False
            
            try:
                if filepath.endswith('.json'):
                    with open(filepath, 'r') as f:
                        session_data = json.load(f)
                else:
                    with open(filepath, 'rb') as f:
                        session_data = pickle.load(f)
            except Exception as e:
                print(f"{Fore.RED}[!] Error loading session: {e}{Style.RESET_ALL}")
                return False
        
        try:
            if format.lower() == "json":
                with open(export_path, 'w') as f:
                    json.dump(session_data, f, indent=2)
            elif format.lower() == "pickle":
                with open(export_path, 'wb') as f:
                    pickle.dump(session_data, f)
            else:
                print(f"{Fore.RED}[!] Unsupported export format: {format}{Style.RESET_ALL}")
                return False
            
            print(f"{Fore.GREEN}[+] Session exported: {export_path}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error exporting session: {e}{Style.RESET_ALL}")
            return False
    
    def import_session(self, import_path: str, session_name: str = None) -> bool:
        if not session_name:
            session_name = os.path.basename(import_path)
        
        if not os.path.exists(import_path):
            print(f"{Fore.RED}[!] Import file not found: {import_path}{Style.RESET_ALL}")
            return False
        
        try:
            if import_path.endswith('.json'):
                with open(import_path, 'r') as f:
                    session_data = json.load(f)
            else:
                with open(import_path, 'rb') as f:
                    session_data = pickle.load(f)
            
            if session_name.endswith('.kts'):
                session_id = session_name.replace('.kts', '')
            else:
                session_id = session_name
            
            session_data['id'] = session_id
            
            if self.use_database:
                self.current_session = session_data
                self._save_to_database(session_id)
            else:
                export_path = os.path.join(self.session_dir, session_name)
                
                if import_path.endswith('.json'):
                    with open(export_path, 'w') as f:
                        json.dump(session_data, f, indent=2)
                else:
                    with open(export_path, 'wb') as f:
                        pickle.dump(session_data, f)
            
            print(f"{Fore.GREEN}[+] Session imported: {session_name}{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[!] Error importing session: {e}{Style.RESET_ALL}")
            return False
    
    def backup_sessions(self, backup_path: str = None) -> str:
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"./sessions_backup_{timestamp}"
        
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        
        try:
            if self.use_database:
                db_path = os.path.join(self.session_dir, "sessions.db")
                backup_db_path = os.path.join(backup_path, "sessions.db")
                shutil.copy2(db_path, backup_db_path)
            
            for filename in os.listdir(self.session_dir):
                if filename.endswith('.kts'):
                    src_path = os.path.join(self.session_dir, filename)
                    dst_path = os.path.join(backup_path, filename)
                    shutil.copy2(src_path, dst_path)
            
            print(f"{Fore.GREEN}[+] Sessions backed up to: {backup_path}{Style.RESET_ALL}")
            return backup_path
        except Exception as e:
            print(f"{Fore.RED}[!] Error backing up sessions: {e}{Style.RESET_ALL}")
            return None
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        cutoff_date = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        
        try:
            if self.use_database:
                self.db_cursor.execute('DELETE FROM sessions WHERE datetime(created_at) < datetime(?)', (cutoff_date.isoformat(),))
                deleted_count += self.db_cursor.rowcount
                self.db_conn.commit()
            
            for filename in os.listdir(self.session_dir):
                if filename.endswith('.kts'):
                    filepath = os.path.join(self.session_dir, filename)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if mod_time < cutoff_date:
                        os.remove(filepath)
                        deleted_count += 1
            
            print(f"{Fore.GREEN}[+] Cleaned up {deleted_count} old sessions{Style.RESET_ALL}")
            return deleted_count
        except Exception as e:
            print(f"{Fore.RED}[!] Error cleaning up old sessions: {e}{Style.RESET_ALL}")
            return 0
    
    def search_sessions(self, query: str, field: str = "name") -> List[Dict[str, Any]]:
        results = []
        
        if self.use_database:
            if field == "name":
                self.db_cursor.execute('SELECT id, name, start_time, end_time, tags, metadata FROM sessions WHERE name LIKE ?', (f"%{query}%",))
            elif field == "tags":
                self.db_cursor.execute('SELECT id, name, start_time, end_time, tags, metadata FROM sessions WHERE tags LIKE ?', (f"%{query}%",))
            elif field == "target":
                self.db_cursor.execute('''
                SELECT s.id, s.name, s.start_time, s.end_time, s.tags, s.metadata 
                FROM sessions s
                JOIN session_targets t ON s.id = t.session_id
                WHERE t.target LIKE ?
                ''', (f"%{query}%",))
            elif field == "module":
                self.db_cursor.execute('''
                SELECT s.id, s.name, s.start_time, s.end_time, s.tags, s.metadata 
                FROM sessions s
                JOIN session_modules m ON s.id = m.session_id
                WHERE m.module LIKE ?
                ''', (f"%{query}%",))
            
            for row in self.db_cursor.fetchall():
                session_id, name, start_time, end_time, tags, metadata = row
                try:
                    tags_data = json.loads(tags) if tags else []
                    metadata_data = json.loads(metadata) if metadata else {}
                except:
                    tags_data = []
                    metadata_data = {}
                
                results.append({
                    "id": session_id,
                    "name": name,
                    "start_time": start_time,
                    "end_time": end_time,
                    "tags": tags_data,
                    "metadata": metadata_data
                })
        else:
            for filename in os.listdir(self.session_dir):
                if filename.endswith('.kts'):
                    filepath = os.path.join(self.session_dir, filename)
                    
                    try:
                        if filename.endswith('.json'):
                            with open(filepath, 'r') as f:
                                session_data = json.load(f)
                        else:
                            with open(filepath, 'rb') as f:
                                session_data = pickle.load(f)
                        
                        match = False
                        
                        if field == "name" and query.lower() in filename.lower():
                            match = True
                        elif field == "target" and any(query.lower() in target.lower() for target in session_data.get('targets', [])):
                            match = True
                        elif field == "module" and any(query.lower() in module.get('module', '').lower() for module in session_data.get('modules_used', [])):
                            match = True
                        elif field == "tags" and any(query.lower() in tag.lower() for tag in session_data.get('tags', [])):
                            match = True
                        
                        if match:
                            results.append({
                                "name": filename,
                                "path": filepath,
                                "id": session_data.get('id', ''),
                                "start_time": session_data.get('start_time', ''),
                                "end_time": session_data.get('end_time', ''),
                                "tags": session_data.get('tags', []),
                                "metadata": session_data.get('metadata', {})
                            })
                    except Exception as e:
                        print(f"{Fore.RED}[!] Error searching session {filename}: {e}{Style.RESET_ALL}")
        
        return results
    
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
    
    def add_tag(self, tag: str):
        if tag not in self.current_session["tags"]:
            self.current_session["tags"].append(tag)
    
    def remove_tag(self, tag: str):
        if tag in self.current_session["tags"]:
            self.current_session["tags"].remove(tag)
    
    def set_metadata(self, key: str, value: Any):
        self.current_session["metadata"][key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.current_session["metadata"].get(key, default)
    
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
            "notes": [],
            "tags": [],
            "metadata": {}
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
        print(f"{Fore.CYAN}Tags: {', '.join(self.current_session['tags'])}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{'='*60}{Style.RESET_ALL}\n")
    
    def close(self):
        if self.use_database and hasattr(self, 'db_conn'):
            self.db_conn.close()
        
        if self._auto_save_thread and self._auto_save_thread.is_alive():
            self.stop_auto_save()
