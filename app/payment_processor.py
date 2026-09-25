import hashlib
import logging
import requests
from app.models import PaymentRequest, PaymentResponse

logger = logging.getLogger("payment_processor")
logger.setLevel(logging.INFO)

def generate_transaction_hash(card_number: str) -> str:
    # FALLO TÉCNICO: Algoritmo deprecado por la guía técnica (genera 40 chars)
    return hashlib.sha1(card_number.encode("utf-8")).hexdigest()

def process_transaction(payment: PaymentRequest) -> PaymentResponse:
    # FALLO DE COMPLIANCE: Imprime el número completo de tarjeta (PAN) en texto plano
    logger.info(f"Processing payment of ${payment.amount} for card: {payment.card_number}")

    token = generate_transaction_hash(payment.card_number)

    try:
        # FALLO TÉCNICO: Llamada HTTP síncrona bloqueante a la pasarela bancaria
        response = requests.post(
            "https://httpbin.org/post",
            json={"token": token, "amount": payment.amount},
            timeout=5.0
        )
        status = "COMPLETED" if response.status_code == 200 else "FAILED"
    except Exception as e:
        # FALLO DE COMPLIANCE: Expone la tarjeta en trazas de error
        logger.error(f"Error processing transaction for card {payment.card_number}: {e}")
        status = "ERROR"

    return PaymentResponse(
        transaction_id="TX-100234",
        status=status,
        token=token
    )