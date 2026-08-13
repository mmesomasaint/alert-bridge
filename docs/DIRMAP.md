alert-bridge/
├── app/
│   ├── __init__.py
│   ├── main.py                   # App startup, lifespan, security middleware & global exception handlers
│   ├── config.py                 # Pydantic Settings with strict secret validation
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py         # V1 API Router aggregation
│   │       └── endpoints.py      # Inbound Webhook ingestion & alert health check routes
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py       # HMAC-SHA256 signature verification & XSS/HTML sanitization
│   │   ├── rate_limiter.py   # Sliding-window rate limiter against DDoS/webhook spam
│   │   └── database.py       # Async SQLAlchemy engine for audit logging & idempotency tracking
│   ├── models/
│   │   ├── __init__.py
│   │   └── payload.py            # SQLAlchemy model for persistent event audit logging
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── payload.py            # Pydantic models for incoming webhooks & outbound dispatch
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser_service.py     # Dynamic payload normalizing engine (Typeform/Google Forms -> Standard)
│   │   ├── sms_service.py        # Twilio SMS / WhatsApp API client with fallback retry loops
│   │   └── email_service.py      # Async SMTP / SendGrid backup notification mailer
│   └── templates/
│       └── lead_alert.html       # HTML Email fallback template for high-priority leads
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Async Pytest fixtures, mock webhooks, and test DB session
│   ├── test_security.py          # HMAC verification & signature spoofing tests
│   ├── test_parser.py            # Unstructured payload normalizing tests
│   └── test_api.py               # Webhook ingestion & dispatch integration tests
├── devops/
│   ├── docker-compose.yml        # Multi-container stack (API, PostgreSQL, Redis, Mailpit)
│   ├── Dockerfile                # Production multi-stage secure container build
│   └── nginx.conf                # Reverse proxy with TLS, security headers, and rate limits
├── docs/
│   └── ARCHITECTURE.md           # System Architecture & Threat Model Documentation
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md                     # Technical handover & deployment documentation
└── requirements.txt              # Locked dependencies
