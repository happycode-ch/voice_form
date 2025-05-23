"""
File: backend/app/api/health.py
Description: Health check and system status endpoints with API key verification.
AI-hints:
- Provides /health for basic service status
- Provides /health/openai for API key verification
- Returns detailed configuration status in development
- Handles graceful degradation when APIs are unavailable
"""
import logging
from typing import Any, Dict

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import config
from app.db.session import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def basic_health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "voiceform-api"}


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Detailed health check including all system components.

    Returns:
        Comprehensive system status including:
        - Database connectivity
        - OpenAI API status
        - Configuration summary
        - Service availability
    """
    health_status = {
        "status": "healthy",
        "timestamp": None,
        "version": "1.0.0",
        "environment": config.environment,
        "components": {
            "database": await _check_database_health(db),
            "openai_api": await _check_openai_health(),
            "configuration": _check_configuration_health(),
        },
    }

    # Determine overall status
    component_statuses = [comp["status"] for comp in health_status["components"].values()]
    if "unhealthy" in component_statuses:
        health_status["status"] = "unhealthy"
    elif "degraded" in component_statuses:
        health_status["status"] = "degraded"

    # Add timestamp
    from datetime import datetime

    health_status["timestamp"] = datetime.utcnow().isoformat() + "Z"

    # Return appropriate HTTP status
    status_code = 200
    if health_status["status"] == "unhealthy":
        status_code = 503
    elif health_status["status"] == "degraded":
        status_code = 200  # Still operational

    return JSONResponse(content=health_status, status_code=status_code)


@router.get("/openai")
async def verify_openai_api():
    """
    Verify OpenAI API key and service availability.

    Returns:
        OpenAI API status and configuration details
    """
    if config.use_mock_transcription and config.use_mock_summarization:
        return {
            "status": "mock_mode",
            "message": "Running in mock mode - OpenAI API not used",
            "mock_transcription": config.use_mock_transcription,
            "mock_summarization": config.use_mock_summarization,
        }

    if not config.openai_api_key:
        raise HTTPException(
            status_code=424,  # Failed Dependency
            detail="OpenAI API key not configured",
        )

    # Test the API key with a minimal request
    try:
        headers = {
            "Authorization": f"Bearer {config.openai_api_key}",
            "Content-Type": "application/json",
        }

        # Use models endpoint for lightweight verification
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.openai.com/v1/models", headers=headers, timeout=10.0
            )

            if response.status_code == 200:
                models_data = response.json()
                available_models = [model["id"] for model in models_data.get("data", [])]

                return {
                    "status": "healthy",
                    "message": "OpenAI API key verified successfully",
                    "configured_model": config.openai_model,
                    "model_available": config.openai_model in available_models,
                    "total_models": len(available_models),
                }
            else:
                error_detail = response.json().get("error", {}).get("message", "Unknown error")
                raise HTTPException(
                    status_code=424,
                    detail=f"OpenAI API verification failed: {error_detail}",
                )

    except httpx.TimeoutException:
        raise HTTPException(status_code=424, detail="OpenAI API verification timed out")
    except Exception as e:
        logger.exception("Error verifying OpenAI API")
        raise HTTPException(status_code=424, detail=f"OpenAI API verification failed: {str(e)}")


async def _check_database_health(db: Session) -> Dict[str, Any]:
    """Check database connectivity and basic operations."""
    try:
        # Simple query to test connection - use text() for modern SQLAlchemy
        result = db.execute(text("SELECT 1"))
        result.fetchone()

        return {
            "status": "healthy",
            "message": "Database connection successful",
            "url": config.database_url.split("@")[-1]
            if "@" in config.database_url
            else "configured",
        }
    except Exception as e:
        logger.exception("Database health check failed")
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
        }


async def _check_openai_health() -> Dict[str, Any]:
    """Check OpenAI API availability."""
    if config.use_mock_transcription and config.use_mock_summarization:
        return {
            "status": "mock_mode",
            "message": "Running in mock mode",
            "mock_transcription": True,
            "mock_summarization": True,
        }

    if not config.openai_api_key:
        return {
            "status": "degraded",
            "message": "OpenAI API key not configured - using mock mode",
            "mock_transcription": config.use_mock_transcription,
            "mock_summarization": config.use_mock_summarization,
        }

    try:
        headers = {"Authorization": f"Bearer {config.openai_api_key}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.openai.com/v1/models", headers=headers, timeout=5.0
            )

            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "message": "OpenAI API accessible",
                    "configured_model": config.openai_model,
                }
            else:
                return {
                    "status": "degraded",
                    "message": f"OpenAI API error: {response.status_code}",
                }

    except Exception as e:
        return {"status": "degraded", "message": f"OpenAI API check failed: {str(e)}"}


def _check_configuration_health() -> Dict[str, Any]:
    """Check configuration validity."""
    try:
        # Configuration is validated on startup, so if we're here it's valid
        return {
            "status": "healthy",
            "message": "Configuration valid",
            "environment": config.environment,
            "debug_mode": config.debug,
            "max_file_size_mb": config.max_audio_file_size_mb,
            "rate_limit_per_minute": config.rate_limit_per_minute,
        }
    except Exception as e:
        return {"status": "unhealthy", "message": f"Configuration error: {str(e)}"}
