# app/core/security.py
import hmac
import hashlib
import bleach
from fastapi import Request, HTTPException, status
from app.config import settings

def verify_hmac_signature(raw_body: bytes, signature_header: str) -> bool:
    """
    Validates HMAC-SHA256 signature against inbound payload bytes to ensure
    authenticity of originating webhook source.
    """
    if not signature_header:
        return False
        
    secret_bytes = settings.WEBHOOK_SECRET.get_secret_value().encode('utf-8')
    
    # Handle signature prefixes e.g. "sha256=..."
    if signature_header.startswith("sha256="):
        expected_hash = signature_header.split("sha256=")[1]
    else:
        expected_hash = signature_header

    computed_hash = hmac.new(secret_bytes, raw_body, hashlib.sha256).hexdigest()
    
    # Constant time comparison prevents timing attacks
    return hmac.compare_digest(computed_hash, expected_hash)

def sanitize_text(text_content: str) -> str:
    """
    Sanitizes raw form field content, stripping any embedded HTML, script tags, 
    or harmful characters before sending to SMS / Mail handlers.
    """
    if not isinstance(text_content, str):
        return str(text_content)
        
    # Completely strip all HTML tags and strip trailing white spaces
    clean_text = bleach.clean(text_content, tags=[], strip=True)
    return clean_text.strip()
