from pydantic import BaseModel, Field

class PaymentRequest(BaseModel):
    customer_id: str
    card_number: str = Field(..., description="Card number to be charged")
    expiry: str
    cvv: str
    amount: float

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    token: str
    masked_card: str | None = None