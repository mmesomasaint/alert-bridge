# tests/test_api.py
import pytest
import hmac
import hashlib
from app.config import settings

@pytest.mark.asyncio
async def test_webhook_ingestion_and_deduplication(client):
    payload = {
        "form_title": "Contact Us",
        "Full Name": "John Doe",
        "Email": "john@example.com",
        "Message": "Interested in enterprise tier pricing."
    }

    # First request
    res1 = await client.post("/api/v1/webhooks/google_forms", json=payload)
    assert res1.status_code == 200
    assert res1.json()["status"] == "accepted"
    assert res1.json()["deduplicated"] is False

    # Immediate duplicate request should trigger deduplication guard
    res2 = await client.post("/api/v1/webhooks/google_forms", json=payload)
    assert res2.status_code == 200
    assert res2.json()["deduplicated"] is True
