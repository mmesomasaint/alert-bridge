# Webhook-to-Email & SMS Alert Bridge (`alert-bridge`)

An enterprise-ready microservice built with **FastAPI**, **Twilio**, **PostgreSQL**, and **aiosmtplib** that ingests webhooks from form services (`Typeform, Google Forms, Custom HTML Forms`), normalizes unstructured payload data, and dispatches real-time SMS/WhatsApp and HTML Email notifications to small business owners.

## Key Features
- **HMAC-SHA256 Security:** Cryptographically verifies incoming webhook signatures to block origin spoofing.
- **XSS & HTML Sanitization:** Filters all field inputs via `bleach` to prevent code injection attacks.
- **Idempotency Guard:** Uses `SHA-256` body hashing to drop duplicate webhooks and prevent SMS budget drain.
- **Failover Notifications:** Sends SMS/WhatsApp instantly via `Twilio`, with automatic fallback to async HTML emails.

---

## Local Quick Start

1. **Activate Virtual Environment & Install Dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   ```

3. **Start Mock SMTP & FastAPI Application:**
   - Terminal 1 (Mock SMTP):
     ```bash
     python -m aiosmtpd -n -l localhost:3025
     ```

   - Terminal 2 (FastAPI Application):
     ```bash
     uvicorn app.main:app --reload --port 8000
     ```

--- 

## Interactive Testing (Swagger UI)

1. Open `http://localhost:8000/docs` in your browser.
2. Expand `POST /api/v1/webhooks/{source_slug}` (e.g. `/api/v1/webhooks/google_forms`).
3. Click Try it out and execute with sample JSON:
   ```JSON
   {
    "form_title": "Website Inquiry",
    "Full Name": "Alice Morgan",
    "Email": "alice@company.com",
    "Phone": "+1987654321",
    "Message": "We need a custom software quote immediately.",
   }
    ```
4. Check Terminal 2 logs for SMS dispatch output and open `http://localhost:8025` (if using Docker Mailpit) or Terminal 1 for raw email logs.

---

## Run Pytest Suite

```bash
pytest -v
```
