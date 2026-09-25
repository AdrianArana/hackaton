import logging
from fastapi import FastAPI, Request

app = FastAPI()
logger = logging.getLogger("payment-service")

@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    body = await request.body()
    logger.info(f"RAW REQUEST: {body}")  # ROTO: vuelca body crudo (puede tener PAN)
    return await call_next(request)