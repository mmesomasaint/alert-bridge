# app/schemas/payload.py
from pydantic import BaseModel, Field, EmailStr
from typing import Dict, Any, Optional
from datetime import datetime

class StandardizedLeadSchema(BaseModel):
    lead_name: str = Field(default="Valued Prospect")
    lead_email: Optional[EmailStr] = None
    lead_phone: Optional[str] = None
    message: str = Field(default="No message body supplied.")
    form_title: str = Field(default="Inbound Webhook Lead")
    raw_fields: Dict[str, Any] = Field(default_factory=dict)

class WebhookIngestResponse(BaseModel):
    status: str
    event_id: str
    message: str
    deduplicated: bool = False
