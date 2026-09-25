import hashlib
import requests

def generate_transaction_hash(payload: str) -> str:
    return hashlib.sha1(payload.encode()).hexdigest()  # ROTO: SHA-1

def verify_with_processor(transaction_id: str, payload: dict) -> dict:
    response = requests.post(  # ROTO: síncrono
        "https://processor.internal/verify",
        json={"transaction_id": transaction_id, "payload": payload},
    )
    return response.json()