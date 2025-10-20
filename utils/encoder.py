import urllib.parse
import base64
import html
import hashlib
import binascii
import string
from typing import List, Tuple, Union, Optional
from itertools import cycle

class PayloadEncoder:
    @staticmethod
    def url_encode(payload: str) -> str:
        return urllib.parse.quote(payload)
    
    @staticmethod
    def double_url_encode(payload: str) -> str:
        return urllib.parse.quote(urllib.parse.quote(payload))
    
    @staticmethod
    def base64_encode(payload: str) -> str:
        return base64.b64encode(payload.encode()).decode()
    
    @staticmethod
    def base64_url_safe_encode(payload: str) -> str:
        return base64.urlsafe_b64encode(payload.encode()).decode()
    
    @staticmethod
    def html_encode(payload: str) -> str:
        return html.escape(payload)
    
    @staticmethod
    def hex_encode(payload: str) -> str:
        return ''.join([hex(ord(c))[2:] for c in payload])
    
    @staticmethod
    def unicode_encode(payload: str) -> str:
        return ''.join([f'\\u{ord(c):04x}' for c in payload])
    
    @staticmethod
    def rot13_encode(payload: str) -> str:
        return payload.translate(str.maketrans(
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
        ))
    
    @staticmethod
    def caesar_cipher(payload: str, shift: int) -> str:
        result = ""
        for char in payload:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    @staticmethod
    def xor_cipher(payload: str, key: str) -> str:
        return ''.join([chr(ord(c) ^ ord(k)) for c, k in zip(payload, cycle(key))])
    
    @staticmethod
    def md5_hash(payload: str) -> str:
        return hashlib.md5(payload.encode()).hexdigest()
    
    @staticmethod
    def sha1_hash(payload: str) -> str:
        return hashlib.sha1(payload.encode()).hexdigest()
    
    @staticmethod
    def sha256_hash(payload: str) -> str:
        return hashlib.sha256(payload.encode()).hexdigest()
    
    @staticmethod
    def char_code_encode(payload: str) -> str:
        return ','.join([str(ord(c)) for c in payload])
    
    @staticmethod
    def binary_encode(payload: str) -> str:
        return ' '.join([format(ord(c), '08b') for c in payload])
    
    @staticmethod
    def octal_encode(payload: str) -> str:
        return '\\'.join([format(ord(c), 'o') for c in payload])
    
    @staticmethod
    def encode_all(payload: str) -> List[Tuple[str, str]]:
        encodings = []
        encodings.append(("Original", payload))
        encodings.append(("URL Encoded", PayloadEncoder.url_encode(payload)))
        encodings.append(("Double URL Encoded", PayloadEncoder.double_url_encode(payload)))
        encodings.append(("Base64 Encoded", PayloadEncoder.base64_encode(payload)))
        encodings.append(("Base64 URL Safe Encoded", PayloadEncoder.base64_url_safe_encode(payload)))
        encodings.append(("HTML Encoded", PayloadEncoder.html_encode(payload)))
        encodings.append(("Hex Encoded", PayloadEncoder.hex_encode(payload)))
        encodings.append(("Unicode Encoded", PayloadEncoder.unicode_encode(payload)))
        encodings.append(("ROT13 Encoded", PayloadEncoder.rot13_encode(payload)))
        encodings.append(("Caesar Cipher (shift=3)", PayloadEncoder.caesar_cipher(payload, 3)))
        encodings.append(("XOR Cipher (key='koto')", PayloadEncoder.xor_cipher(payload, "koto")))
        encodings.append(("MD5 Hash", PayloadEncoder.md5_hash(payload)))
        encodings.append(("SHA1 Hash", PayloadEncoder.sha1_hash(payload)))
        encodings.append(("SHA256 Hash", PayloadEncoder.sha256_hash(payload)))
        encodings.append(("Character Code", PayloadEncoder.char_code_encode(payload)))
        encodings.append(("Binary", PayloadEncoder.binary_encode(payload)))
        encodings.append(("Octal", PayloadEncoder.octal_encode(payload)))
        return encodings

class PayloadDecoder:
    @staticmethod
    def url_decode(payload: str) -> str:
        return urllib.parse.unquote(payload)
    
    @staticmethod
    def base64_decode(payload: str) -> str:
        try:
            return base64.b64decode(payload).decode()
        except Exception:
            return "Invalid Base64"
    
    @staticmethod
    def base64_url_safe_decode(payload: str) -> str:
        try:
            return base64.urlsafe_b64decode(payload).decode()
        except Exception:
            return "Invalid Base64 URL Safe"
    
    @staticmethod
    def html_decode(payload: str) -> str:
        return html.unescape(payload)
    
    @staticmethod
    def hex_decode(payload: str) -> str:
        try:
            return bytes.fromhex(payload).decode()
        except Exception:
            return "Invalid Hex"
    
    @staticmethod
    def unicode_decode(payload: str) -> str:
        try:
            return payload.encode().decode('unicode-escape')
        except Exception:
            return "Invalid Unicode"
    
    @staticmethod
    def rot13_decode(payload: str) -> str:
        return payload.translate(str.maketrans(
            'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM',
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ))
    
    @staticmethod
    def caesar_decipher(payload: str, shift: int) -> str:
        return PayloadEncoder.caesar_cipher(payload, -shift)
    
    @staticmethod
    def xor_decipher(payload: str, key: str) -> str:
        return PayloadEncoder.xor_cipher(payload, key)
    
    @staticmethod
    def char_code_decode(payload: str) -> str:
        try:
            return ''.join([chr(int(c)) for c in payload.split(',')])
        except Exception:
            return "Invalid Character Code"
    
    @staticmethod
    def binary_decode(payload: str) -> str:
        try:
            return ''.join([chr(int(binary, 2)) for binary in payload.split()])
        except Exception:
            return "Invalid Binary"
    
    @staticmethod
    def octal_decode(payload: str) -> str:
        try:
            return ''.join([chr(int(octal, 8)) for octal in payload.split('\\') if octal])
        except Exception:
            return "Invalid Octal"
    
    @staticmethod
    def decode_all(payload: str) -> List[Tuple[str, str]]:
        decodings = []
        decodings.append(("Original", payload))
        decodings.append(("URL Decoded", PayloadDecoder.url_decode(payload)))
        decodings.append(("Base64 Decoded", PayloadDecoder.base64_decode(payload)))
        decodings.append(("Base64 URL Safe Decoded", PayloadDecoder.base64_url_safe_decode(payload)))
        decodings.append(("HTML Decoded", PayloadDecoder.html_decode(payload)))
        decodings.append(("Hex Decoded", PayloadDecoder.hex_decode(payload)))
        decodings.append(("Unicode Decoded", PayloadDecoder.unicode_decode(payload)))
        decodings.append(("ROT13 Decoded", PayloadDecoder.rot13_decode(payload)))
        decodings.append(("Caesar Decipher (shift=3)", PayloadDecoder.caesar_decipher(payload, 3)))
        decodings.append(("XOR Decipher (key='koto')", PayloadDecoder.xor_decipher(payload, "koto")))
        decodings.append(("Character Code Decoded", PayloadDecoder.char_code_decode(payload)))
        decodings.append(("Binary Decoded", PayloadDecoder.binary_decode(payload)))
        decodings.append(("Octal Decoded", PayloadDecoder.octal_decode(payload)))
        return decodings

class PayloadAnalyzer:
    @staticmethod
    def analyze(payload: str) -> dict:
        analysis = {
            "length": len(payload),
            "character_types": {
                "letters": sum(c.isalpha() for c in payload),
                "digits": sum(c.isdigit() for c in payload),
                "special": sum(not c.isalnum() for c in payload),
                "spaces": sum(c.isspace() for c in payload)
            },
            "encoding_indicators": {
                "looks_like_base64": PayloadAnalyzer._looks_like_base64(payload),
                "looks_like_hex": PayloadAnalyzer._looks_like_hex(payload),
                "looks_like_url_encoded": PayloadAnalyzer._looks_like_url_encoded(payload),
                "looks_like_html_encoded": PayloadAnalyzer._looks_like_html_encoded(payload),
                "looks_like_unicode": PayloadAnalyzer._looks_like_unicode(payload),
                "looks_like_char_code": PayloadAnalyzer._looks_like_char_code(payload),
                "looks_like_binary": PayloadAnalyzer._looks_like_binary(payload),
                "looks_like_octal": PayloadAnalyzer._looks_like_octal(payload)
            },
            "entropy": PayloadAnalyzer._calculate_entropy(payload),
            "suggested_decodings": []
        }
        
        for encoding_name, decoder in [
            ("URL", PayloadDecoder.url_decode),
            ("Base64", PayloadDecoder.base64_decode),
            ("Base64 URL Safe", PayloadDecoder.base64_url_safe_decode),
            ("HTML", PayloadDecoder.html_decode),
            ("Hex", PayloadDecoder.hex_decode),
            ("Unicode", PayloadDecoder.unicode_decode),
            ("ROT13", PayloadDecoder.rot13_decode),
            ("Character Code", PayloadDecoder.char_code_decode),
            ("Binary", PayloadDecoder.binary_decode),
            ("Octal", PayloadDecoder.octal_decode)
        ]:
            try:
                decoded = decoder(payload)
                if decoded != payload and not decoded.startswith("Invalid"):
                    analysis["suggested_decodings"].append((encoding_name, decoded))
            except:
                pass
        
        return analysis
    
    @staticmethod
    def _looks_like_base64(payload: str) -> bool:
        try:
            return len(payload) % 4 == 0 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=" for c in payload)
        except:
            return False
    
    @staticmethod
    def _looks_like_hex(payload: str) -> bool:
        try:
            return len(payload) % 2 == 0 and all(c in "0123456789abcdefABCDEF" for c in payload)
        except:
            return False
    
    @staticmethod
    def _looks_like_url_encoded(payload: str) -> bool:
        return "%" in payload and len(payload) >= 3
    
    @staticmethod
    def _looks_like_html_encoded(payload: str) -> bool:
        return "&" in payload and ";" in payload
    
    @staticmethod
    def _looks_like_unicode(payload: str) -> bool:
        return "\\u" in payload
    
    @staticmethod
    def _looks_like_char_code(payload: str) -> bool:
        try:
            parts = payload.split(',')
            return len(parts) > 1 and all(part.isdigit() for part in parts)
        except:
            return False
    
    @staticmethod
    def _looks_like_binary(payload: str) -> bool:
        try:
            parts = payload.split()
            return len(parts) > 1 and all(part in "01" for part in parts)
        except:
            return False
    
    @staticmethod
    def _looks_like_octal(payload: str) -> bool:
        try:
            parts = payload.split('\\')
            return len(parts) > 1 and all(part in "01234567" for part in parts if part)
        except:
            return False
    
    @staticmethod
    def _calculate_entropy(payload: str) -> float:
        if not payload:
            return 0.0
        
        entropy = 0.0
        for char in set(payload):
            p = payload.count(char) / len(payload)
            entropy -= p * (p and binascii.log2(p))
        
        return entropy
