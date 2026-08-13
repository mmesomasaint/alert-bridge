# app/api/v1/endpoints.py
import hashlib
import json
from fastapi import APIRouter, Request, BackgroundTasks, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db, AsyncSessionLocal
from app.core.security import verify_hmac_signature
from app.models.payload import WebhookEventModel
from app.schemas.payload import WebhookIngestResponse
from app.services.parser_service import parser_service
from app.services.sms_service import sms_service
from app.services.email_service import email_service
from app.config import settings

router = APIRouter()

async def process_webhook_alert_background(event_id: str, source_slug: str, raw_json: dict):
    """Background worker task handling normalization, SMS, and Email delivery."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(WebhookEventModel).filter(WebhookEventModel.id == event_id))
        event = result.scalars().first()
        if not event:
            return

        try:
            # Parse & Sanitize raw payload
            lead = parser_service.parse_payload(source_slug, raw_json)
            event.sanitized_data = lead.model_dump()

            # Primary SMS/WhatsApp Alert
            sms_ok = sms_service.send_alert(lead)
            event.sms_sent = sms_ok

            # Always dispatch fallback email
            email_ok = await email_service.send_lead_fallback_email(lead)
            event.email_sent = email_ok

            event.processed = True
        except Exception as e:
            event.error_log = str(e)

        await db.commit()

@router.post("/{source_slug}", response_model=WebhookIngestResponse, status_code=status.HTTP_200_OK)
async def receive_inbound_webhook(
    source_slug: str,
    request: Request,
    background_tasks: BackgroundTasks,
    x_signature: str = Header(default=None, alias="X-Hub-Signature-256"),
    db: AsyncSession = Depends(get_db)
):
    # Enforce payload size limits
    raw_body = await request.body()
    if len(raw_body) > settings.MAX_PAYLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Payload size exceeds 1 MB limit."
        )

    # Cryptographic signature validation in production
    if settings.ENVIRONMENT == "production":
        if not x_signature or not verify_hmac_signature(raw_body, x_signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid HMAC signature header."
            )

    try:
        raw_json = json.loads(raw_body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed JSON body.")

    # Idempotency Deduplication Check (SHA-256 hash of payload body)
    payload_hash = hashlib.sha256(raw_body).hexdigest()
    existing_event = await db.execute(
        select(WebhookEventModel).filter(WebhookEventModel.payload_hash == payload_hash)
    )
    if existing_event.scalars().first():
        return WebhookIngestResponse(
            status="success",
            event_id="deduplicated",
            message="Duplicate webhook payload ignored.",
            deduplicated=True
        )

    # Persist Event Record
    event = WebhookEventModel(
        source=source_slug,
        payload_hash=payload_hash,
        sanitized_data={}
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    # Hand off to background worker
    background_tasks.add_task(
        process_webhook_alert_background,
        event.id,
        source_slug,
        raw_json
    )

    return WebhookIngestResponse(
        status="accepted",
        event_id=event.id,
        message="Webhook ingested and alert queued."
    )
