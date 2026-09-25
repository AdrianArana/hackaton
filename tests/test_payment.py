from app.payment_processor import generate_transaction_hash

def test_hash_length_sha1():
    result = generate_transaction_hash("tx-12345")
    assert len(result) == 40  # Espera SHA-1 → esto es lo que Subagente 3 tendrá que corregir