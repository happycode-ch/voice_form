"""
File: backend/app/main.py
Description: FastAPI application entry point with configuration validation and startup checks.
AI-hints:
- Validates configuration on startup using centralized config system
- Sets up structured logging based on config
- Includes startup and shutdown event handlers
- Provides graceful error handling for configuration issues
- Handles container dependencies and startup timing
"""
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router as api_router
from app.config import ConfigurationError, config

# Configure logging based on configuration
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


async def wait_for_dependencies():
    """Wait for container dependencies to be ready."""
    logger.info("🔍 Checking container dependencies...")

    # Import here to avoid circular imports and to handle DB connection timing
    from sqlalchemy import text

    from app.db.session import engine

    # Test database connectivity
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            db_version = result.fetchone()[0]
            logger.info(f"✅ Database ready: {db_version.split()[0:2]}")
    except Exception as e:
        logger.warning(f"⚠️ Database not immediately available: {e}")
        # Continue startup - health checks will handle this gracefully

    # Test external services if not in mock mode
    if not config.use_mock_transcription or not config.use_mock_summarization:
        if config.openai_api_key:
            logger.info("🔍 Testing OpenAI API connectivity...")
            try:
                import httpx

                headers = {"Authorization": f"Bearer {config.openai_api_key}"}
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "https://api.openai.com/v1/models",
                        headers=headers,
                        timeout=10.0,
                    )
                    if response.status_code == 200:
                        logger.info("✅ OpenAI API accessible")
                    else:
                        logger.warning(f"⚠️ OpenAI API responded with status {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI API check failed: {e}")

    logger.info("🎯 Dependency checks completed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown tasks."""
    # Startup
    logger.info("🐳 Starting VoiceForm AI application in container...")

    try:
        # Configuration is already validated when config module is imported
        logger.info("✅ Configuration validation completed successfully")

        # Wait for container dependencies
        await wait_for_dependencies()

        # Log startup summary
        logger.info(f"🚀 VoiceForm AI starting in {config.environment} mode")
        if config.use_mock_transcription or config.use_mock_summarization:
            logger.info("⚠️  Running with mock services enabled")

        # Log container-specific information
        db_location = (
            config.database_url.split("@")[-1] if "@" in config.database_url else "configured"
        )
        logger.info(f"🔗 Container networking: Database at {db_location}")

        retry_info = (
            f"{config.database_connection_retries} attempts with "
            f"{config.database_retry_delay_seconds}s delay"
        )
        logger.info(f"🔄 Database retries configured: {retry_info}")

        logger.info("🎯 Container startup completed successfully")

    except ConfigurationError as e:
        logger.error(f"❌ Configuration validation failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"❌ Unexpected startup error: {e}")
        # In containerized environment, we might want to continue with degraded functionality
        logger.warning(
            "⚠️ Starting with potentially degraded functionality - check health endpoints"
        )

    yield

    # Shutdown
    logger.info("🛑 VoiceForm AI container shutting down...")
    logger.info("🔌 Closing database connections...")
    # Database connections will be closed automatically by SQLAlchemy


# Create FastAPI application with configuration-based metadata
app = FastAPI(
    title="VoiceForm AI",
    description="A voice-first, multilingual intake tool for structured questionnaires.",
    version="0.1.2",
    debug=config.debug,
    lifespan=lifespan,
)

# Configure CORS based on environment
cors_origins = (
    ["*"]
    if config.environment == "development"
    else [
        "https://your-production-domain.com"  # TODO: Set actual production domains
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add global exception handler
@app.exception_handler(ConfigurationError)
async def configuration_error_handler(request, exc):
    """Handle configuration errors gracefully."""
    logger.error(f"Configuration error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Server configuration error", "message": str(exc)},
    )


# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with basic service information."""
    return {
        "message": "Welcome to VoiceForm AI",
        "api_url": "/api",
        "health_check": "/api/health",
        "detailed_health": "/api/health/detailed",
        "documentation": "/docs",
        "version": "0.1.2",
        "environment": config.environment,
        "container_mode": True,
    }
