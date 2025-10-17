"""Configuration management for Kotosploit"""

import json
import os
from typing import Dict, Any

class Config:
    def __init__(self, config_file: str = "kotosploit.conf"):
        self.config_file = config_file
        self.settings = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        default_config = {
            "general": {
                "timeout": 10,
                "user_agent": "Kotosploit/1.0",
                "verify_ssl": False,
                "max_threads": 10,
                "verbose": True
            },
            "scanner": {
                "sqli": {
                    "enabled": True,
                    "payloads": "default",
                    "detection_threshold": 1
                },
                "xss": {
                    "enabled": True,
                    "payloads": "default",
                    "detection_threshold": 1
                },
                "lfi": {
                    "enabled": True,
                    "payloads": "default",
                    "detection_threshold": 1
                },
                "cmdi": {
                    "enabled": True,
                    "payloads": "default",
                    "detection_threshold": 1
                }
            },
            "reporting": {
                "auto_save": True,
                "format": "json",
                "directory": "./reports"
            },
            "network": {
                "proxy": None,
                "proxy_type": "http",
                "retry_attempts": 3,
                "retry_delay": 1
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception:
                pass
        
        return default_config
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        keys = key.split('.')
        current = self.settings
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
