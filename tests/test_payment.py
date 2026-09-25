from app.payment_processor import generate_transaction_hash


def test_hash_length_hmac_sha256():
    """Token must be 64 hex characters (HMAC-SHA256)."""
    result = generate_transaction_hash("tx-12345")
    assert len(result) == 64, f"Expected 64-char HMAC-SHA256 token, got {len(result)}"


def test_hash_is_hex_string():
    """Token must consist only of lowercase hex digits."""
    result = generate_transaction_hash("tx-12345")
    assert all(c in "0123456789abcdef" for c in result)


def test_hash_deterministic():
    """Same input with same key must always produce the same token."""
    assert generate_transaction_hash("4532123456788921") == generate_transaction_hash("4532123456788921")