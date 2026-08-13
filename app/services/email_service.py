# app/services/email_service.py
import aiosmtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os
from app.config import settings
from app.schemas.payload import StandardizedLeadSchema

class EmailService:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), "../templates")
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    async def send_lead_fallback_email(self, lead: StandardizedLeadSchema) -> bool:
        """Sends comprehensive HTML notification email to owner."""
        template = self.jinja_env.get_template("lead_alert.html")
        rendered_html = template.render(lead=lead)

        msg = EmailMessage()
        msg["Subject"] = f"New Lead Alert: {lead.lead_name} ({lead.form_title})"
        msg["From"] = settings.EMAILS_FROM_EMAIL
        msg["To"] = settings.OWNER_EMAIL
        msg.set_content(
            f"New lead received from {lead.lead_name}.\nEmail: {lead.lead_email}\nMessage: {lead.message}"
        )
        msg.add_alternative(rendered_html, subtype="html")

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER if settings.SMTP_USER else None,
                password=settings.SMTP_PASSWORD.get_secret_value() if settings.SMTP_USER else None
            )
            print(f"Backup Alert Email sent to {settings.OWNER_EMAIL}")
            return True
        except Exception as e:
            print(f"Email Dispatch Error: {e}")
            return False

email_service = EmailService()
