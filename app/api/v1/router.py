# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import router as webhook_router

api_router = APIRouter()
api_router.include_router(webhook_router, prefix="/webhooks", tags=["Inbound Webhooks"])
