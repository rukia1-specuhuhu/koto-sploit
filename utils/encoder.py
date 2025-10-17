"""Payload encoder/decoder utilities"""

import urllib.parse
import base64
import html
from typing import List

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
    def html_encode(payload: str) -> str:
        return html.escape(payload)
    
    @staticmethod
    def hex_encode(payload: str) -> str:
        return ''.join([hex(ord(c))[2:] for c in payload])
    
    @staticmethod
    def unicode_encode(payload: str) -> str:
        return ''.join([f'\\u{ord(c):04x}' for c in payload])
    
    @staticmethod
    def encode_all(payload: str) -> List[tuple]:
        encodings = []
        encodings.append(("Original", payload))
        encodings.append(("URL Encoded", PayloadEncoder.url_encode(payload)))
        encodings.append(("Double URL Encoded", PayloadEncoder.double_url_encode(payload)))
        encodings.append(("Base64 Encoded", PayloadEncoder.base64_encode(payload)))
        encodings.append(("HTML Encoded", PayloadEncoder.html_encode(payload)))
        encodings.append(("Hex Encoded", PayloadEncoder.hex_encode(payload)))
        encodings.append(("Unicode Encoded", PayloadEncoder.unicode_encode(payload)))
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
    def html_decode(payload: str) -> str:
        return html.unescape(payload)
    
    @staticmethod
    def decode_all(payload: str) -> List[tuple]:
        decodings = []
        decodings.append(("Original", payload))
        decodings.append(("URL Decoded", PayloadDecoder.url_decode(payload)))
        decodings.append(("Base64 Decoded", PayloadDecoder.base64_decode(payload)))
        decodings.append(("HTML Decoded", PayloadDecoder.html_decode(payload)))
        return decodings
