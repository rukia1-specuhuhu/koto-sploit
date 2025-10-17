"""Module loader system for Kotosploit"""

import importlib
import os
from typing import Dict, Optional
from modules.base import BaseModule

class ModuleLoader:
    def __init__(self):
        self.modules = {}
        self._scan_modules()
    
    def _scan_modules(self):
        module_paths = {
            "exploit": "modules.exploits",
            "auxiliary": "modules.auxiliary",
        }
        
        for module_type, base_path in module_paths.items():
            try:
                package = importlib.import_module(base_path)
                if package.__file__ is None:
                    continue
                package_dir = os.path.dirname(package.__file__)
                
                for filename in os.listdir(package_dir):
                    if filename.endswith('.py') and filename != '__init__.py':
                        module_name = filename[:-3]
                        full_path = f"{base_path}.{module_name}"
                        module_key = f"{module_type}/{module_name}"
                        self.modules[module_key] = full_path
            except Exception:
                pass
    
    def get_module(self, module_path: str) -> Optional[BaseModule]:
        if module_path not in self.modules:
            return None
        
        try:
            module = importlib.import_module(self.modules[module_path])
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BaseModule) and attr != BaseModule:
                    return attr()
        except Exception as e:
            print(f"Error loading module: {e}")
            return None
    
    def list_modules(self) -> Dict[str, str]:
        return self.modules.copy()
