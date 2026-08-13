# app/models/payload.py
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON
from app.core.database import Base
from datetime import datetime, timezone
import uuid

class WebhookEventModel(Base):
    __tablename__ = "webhook_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, nullable=False)               # typeform, google_forms, custom
    payload_hash = Column(String, index=True, nullable=False) # Idempotency deduplication hash
    sanitized_data = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    email_sent = Column(Boolean, default=False)
    error_log = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
