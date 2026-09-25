# Engineering Directive: Deprecation of SHA-1 in Payment Tokenization (RFC-2024-08)

## 1. Context & Vulnerability
Due to collision weaknesses in SHA-1, legacy tokenization in `payment_processor.py` must be decommissioned immediately across all services.

## 2. Mandatory Technical Changes
- Deprecate all usage of `hashlib.sha1()` for token generation.
- Implement `hmac` with `hashlib.sha256` using an application secret key (`os.environ.get("PAYMENT_SECRET_KEY", "default-insecure-key")`).
- Token format must now output a 64-character hex string (up from the legacy 40-character length).
- Replace blocking network calls (`requests.post`) with modern async HTTP execution using `httpx.AsyncClient`.