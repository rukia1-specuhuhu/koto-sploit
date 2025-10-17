"""Base module class for all Kotosploit modules"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseModule(ABC):
    def __init__(self):
        self.options = {}
        self.required_options = []
        self.description = ""
        self.author = "Kotosploit Team"
        self.module_type = "base"
        
    @abstractmethod
    def run(self) -> Dict[str, Any]:
        pass
    
    def set_option(self, name: str, value: Any):
        if name.upper() in self.options:
            self.options[name.upper()] = value
            return True
        return False
    
    def get_option(self, name: str) -> Any:
        return self.options.get(name.upper())
    
    def validate_options(self) -> tuple[bool, str]:
        for opt in self.required_options:
            if not self.options.get(opt):
                return False, f"Required option '{opt}' is not set"
        return True, "OK"
    
    def show_options(self) -> List[tuple]:
        result = []
        for key, value in self.options.items():
            required = "yes" if key in self.required_options else "no"
            result.append((key, str(value), required))
        return result
    
    def get_info(self) -> Dict[str, str]:
        return {
            "name": self.__class__.__name__,
            "description": self.description,
            "author": self.author,
            "type": self.module_type
        }
