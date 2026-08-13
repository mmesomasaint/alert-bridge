# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Webhook Alert Bridge"
    ENVIRONMENT: str = "development"
    
    # API & HMAC Security
    WEBHOOK_SECRET: SecretStr = Field(default=SecretStr("dev_webhook_hmac_secret_998811"))
    API_KEY: SecretStr = Field(default=SecretStr("dev_secret_api_key_12345"))
    MAX_PAYLOAD_SIZE_BYTES: int = 1_048_576  # 1 MB max payload
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./dev_alerts.db",
        env="DATABASE_URL"
    )
    
    # Business Owner Notification Contacts
    OWNER_PHONE_NUMBER: str = Field(default="+1234567890", description="E.164 formatted target phone number")
    OWNER_EMAIL: str = Field(default="owner@business.com")
    
    # Twilio / WhatsApp Provider API Configuration
    TWILIO_ACCOUNT_SID: Optional[str] = Field(default=None)
    TWILIO_AUTH_TOKEN: Optional[SecretStr] = Field(default=None)
    TWILIO_PHONE_NUMBER: Optional[str] = Field(default=None)
    TWILIO_WHATSAPP_NUMBER: Optional[str] = Field(default="whatsapp:+14155238886")
    ENABLE_WHATSAPP: bool = False
    
    # Email / SMTP Configuration
    SMTP_HOST: str = Field(default="localhost")
    SMTP_PORT: int = Field(default=1025)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: SecretStr = Field(default=SecretStr(""))
    EMAILS_FROM_EMAIL: str = Field(default="alerts@bridge.local")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()
