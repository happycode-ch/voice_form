from fastapi import APIRouter
from app.api import transcribe, summarize

router = APIRouter()

# Include sub-routers
router.include_router(transcribe.router, prefix="/transcribe", tags=["transcription"])
router.include_router(summarize.router, prefix="/summarize", tags=["summarization"])

@router.get("/health")
async def health_check():
    """Health check endpoint for the API."""
    return {"status": "healthy"} 