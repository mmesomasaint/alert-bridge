# Architecture Diagram

```Plaintext
[ Inbound Webhook Provider ] 
   (Typeform / Google Forms)
              │
              │  HTTPS POST /api/v1/webhooks/{source_slug}
              │  Headers: X-Typeform-Signature / X-Hub-Signature-256
              ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                       Nginx Proxy                           │
   │  - TLS Termination                                          │
   │  - Rate Limiting (100 req/min per IP)                      │
   │  - Security Headers (HSTS, CSP, X-Frame-Options)            │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                      FastAPI Service                        │
   │  1. HMAC-SHA256 Signature Verification                       │
   │  2. Payload Decompression & Size Verification (< 1MB)       │
   │  3. XSS/HTML Input Scrubbing & Anti-Injection Sanitization   │
   │  4. Idempotency Check (Prevent duplicate webhook alerts)     │
   └──────────────┬──────────────────────────────┬───────────────┘
                  │                              │
                  ▼                              ▼
    ┌───────────────────────────┐  ┌─────────────────────────────┐
    │   PostgreSQL Audit Log    │  │   Async Background Queue    │
    │  - Full Payload Record    │  │  - Parses & Normalizes Data │
    │  - Delivery Status        │  └──────────────┬──────────────┘
    └───────────────────────────┘                 │
                                                  ▼
                                   ┌─────────────────────────────┐
                                   │   Notification Dispatcher   │
                                   ├─────────────────────────────┤
                                   │ Primary:  Twilio SMS/WhatsApp
                                   │ Secondary: Async SMTP Mailer│
                                   └──────────────┬──────────────┘
                                                  │
                                                  ▼
                                       [ Business Owner Device ]
                                         (SMS / WhatsApp / Mail)

```
