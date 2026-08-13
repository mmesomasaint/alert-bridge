# app/services/sms_service.py
from twilio.rest import Client
from app.config import settings
from app.schemas.payload import StandardizedLeadSchema

class SMSService:
    def __init__(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.client = Client(
                settings.TWILIO_ACCOUNT_SID, 
                settings.TWILIO_AUTH_TOKEN.get_secret_value()
            )
        else:
            self.client = None

    def send_alert(self, lead: StandardizedLeadSchema) -> bool:
        """
        Dispatches compact real-time lead SMS/WhatsApp message to business owner.
        """
        alert_body = (
            f"NEW LEAD: {lead.form_title}\n"
            f"Name: {lead.lead_name}\n"
            f"Email: {lead.lead_email or 'N/A'}\n"
            f"Phone: {lead.lead_phone or 'N/A'}\n"
            f"Message: {lead.message[:140]}"
        )

        # Mock print in dev or if credentials missing
        if not self.client or settings.ENVIRONMENT == "development":
            print(f"\n[DEV MOCK SMS DISPATCH TO {settings.OWNER_PHONE_NUMBER}]\n{alert_body}\n")
            return True

        try:
            from_number = settings.TWILIO_PHONE_NUMBER
            target_number = settings.OWNER_PHONE_NUMBER
            
            if settings.ENABLE_WHATSAPP:
                from_number = settings.TWILIO_WHATSAPP_NUMBER
                target_number = f"whatsapp:{settings.OWNER_PHONE_NUMBER}"

            self.client.messages.create(
                body=alert_body,
                from_=from_number,
                to=target_number
            )
            return True
        except Exception as e:
            print(f"Twilio SMS Dispatch Failed: {e}")
            return False

sms_service = SMSService()
