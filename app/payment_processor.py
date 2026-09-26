import hashlib
import hmac
import logging
import os
import httpx
from app.models import PaymentRequest, PaymentResponse

logger = logging.getLogger("payment_processor")
logger.setLevel(logging.INFO)

_SECRET_KEY = os.environ.get("PAYMENT_SECRET_KEY", "default-insecure-key").encode("utf-8")


def _mask_card(card_number: str) -> str:
    """Return first-6 + X-padding + last-4 per PCI-DSS v4 Req 3.4."""
    if len(card_number) <= 10:
        return card_number
    middle = "X" * (len(card_number) - 10)
    return card_number[:6] + middle + card_number[-4:]


def generate_transaction_hash(card_number: str) -> str:
    """Generate a 64-character HMAC-SHA256 hex token."""
    return hmac.new(_SECRET_KEY, card_number.encode("utf-8"), hashlib.sha256).hexdigest()


async def process_transaction(payment: PaymentRequest) -> PaymentResponse:
    masked = _mask_card(payment.card_number)
    logger.info(f"Processing payment of ${payment.amount} for card: {masked}")

    token = generate_transaction_hash(payment.card_number)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://httpbin.org/post",
                json={"token": token, "amount": payment.amount},
                timeout=5.0,
            )
        status = "COMPLETED" if response.status_code == 200 else "FAILED"
    except Exception as e:
        logger.error(f"Error processing transaction for card {masked}: {e}")
        status = "ERROR"

    return PaymentResponse(
        transaction_id="TX-100234",
        status=status,
        token=token,
    )