import json
import logging
from fastapi import FastAPI, Request
from app.models import PaymentRequest, PaymentResponse
from app.payment_processor import process_transaction

app = FastAPI(title="Payment Gateway Service")

logger = logging.getLogger("gateway")
logging.basicConfig(level=logging.INFO)

_SENSITIVE_KEYS = {"card_number", "cvv"}


@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    # PCI-DSS v4 Req 3.4: scrub card_number and cvv before logging
    body_bytes = await request.body()
    try:
        payload = json.loads(body_bytes)
        safe_payload = {k: ("***" if k in _SENSITIVE_KEYS else v) for k, v in payload.items()}
        logger.info(f"Incoming request to {request.url.path}: {safe_payload}")
    except Exception:
        # Non-JSON body: log method + path only, never raw bytes
        logger.info(f"Incoming request to {request.url.path} [{request.method}]")

    response = await call_next(request)
    return response


@app.post("/api/v1/charge", response_model=PaymentResponse)
async def charge_card(payment: PaymentRequest):
    result = await process_transaction(payment)
    return result