"""
File: backend/app/api/routes.py
Description: Main API router configuration with all endpoint groups.
AI-hints:
- Includes transcription, summarization, and health check routes
- Uses prefix-based organization for clean API structure
- Health endpoints provide system status and API verification
"""
from fastapi import APIRouter
from app.api import transcribe, summarize, health

router = APIRouter()

# Include sub-routers with prefixes for clean API organization
router.include_router(transcribe.router, prefix="/transcribe", tags=["transcription"])
router.include_router(summarize.router, prefix="/summarize", tags=["summarization"])
router.include_router(health.router, prefix="/health", tags=["health"]) 