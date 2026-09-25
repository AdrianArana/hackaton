import logging
from fastapi import FastAPI, Request
from app.models import PaymentRequest, PaymentResponse
from app.payment_processor import process_transaction

app = FastAPI(title="Payment Gateway Service")

logger = logging.getLogger("gateway")
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def audit_log_middleware(request: Request, call_next):
    # FALLO DE COMPLIANCE: Vuelca el payload crudo en logs (incluye tarjeta y CVV)
    body = await request.body()
    logger.info(f"Incoming raw request payload: {body.decode('utf-8')}")
    
    response = await call_next(request)
    return response

@app.post("/api/v1/charge", response_model=PaymentResponse)
async def charge_card(payment: PaymentRequest):
    result = process_transaction(payment)
    return result