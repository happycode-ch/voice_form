"""
File: backend/app/config.py
Description: Centralized configuration management with validation and secure defaults.
AI-hints:
- Validates all required environment variables on startup
- Provides graceful fallback to mock mode if OpenAI key missing
- Exposes typed configuration settings via Config class
- Raises ConfigurationError for missing critical settings
- Handles container startup timing with database retry logic
"""
import logging
import os
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""

    pass


class Config:
    """Centralized configuration management with validation."""

    def __init__(self):
        self._validate_configuration()

    # Database Configuration
    @property
    def database_url(self) -> str:
        return os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/voiceform")

    @property
    def database_connection_retries(self) -> int:
        """Number of database connection retries during container startup."""
        return int(os.getenv("DATABASE_CONNECTION_RETRIES", "5"))

    @property
    def database_retry_delay_seconds(self) -> int:
        """Delay between database connection retries in seconds."""
        return int(os.getenv("DATABASE_RETRY_DELAY_SECONDS", "2"))

    # OpenAI Configuration
    @property
    def openai_api_key(self) -> Optional[str]:
        return os.getenv("OPENAI_API_KEY")

    @property
    def openai_model(self) -> str:
        return os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Mock Mode Configuration
    @property
    def use_mock_transcription(self) -> bool:
        return os.getenv("USE_MOCK_TRANSCRIPTION", "False").lower() == "true"

    @property
    def use_mock_summarization(self) -> bool:
        return os.getenv("USE_MOCK_SUMMARIZATION", "False").lower() == "true"

    # Application Settings
    @property
    def environment(self) -> str:
        return os.getenv("ENVIRONMENT", "development")

    @property
    def debug(self) -> bool:
        return os.getenv("DEBUG", "false").lower() == "true"

    @property
    def log_level(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO").upper()

    # Security & Performance Settings
    @property
    def max_audio_file_size_mb(self) -> int:
        return int(os.getenv("MAX_AUDIO_FILE_SIZE_MB", "25"))

    @property
    def max_audio_duration_seconds(self) -> int:
        return int(os.getenv("MAX_AUDIO_DURATION_SECONDS", "300"))

    @property
    def request_timeout_seconds(self) -> int:
        return int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))

    @property
    def rate_limit_per_minute(self) -> int:
        return int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # Container-specific settings
    @property
    def container_startup_timeout_seconds(self) -> int:
        """Maximum time to wait for all container dependencies during startup."""
        return int(os.getenv("CONTAINER_STARTUP_TIMEOUT_SECONDS", "60"))

    def _validate_configuration(self):
        """Validate configuration and provide helpful error messages."""
        errors = []
        warnings = []

        # Validate database URL
        if not self.database_url:
            errors.append("DATABASE_URL is required")

        # Validate OpenAI configuration if not in mock mode
        if not self.use_mock_transcription or not self.use_mock_summarization:
            if not self.openai_api_key:
                if self.environment == "production":
                    errors.append(
                        "OPENAI_API_KEY is required in production when mock mode is disabled"
                    )
                else:
                    warnings.append("OPENAI_API_KEY is missing - falling back to mock mode")
                    # Auto-enable mock mode if no API key in development
                    os.environ["USE_MOCK_TRANSCRIPTION"] = "true"
                    os.environ["USE_MOCK_SUMMARIZATION"] = "true"
            elif self.openai_api_key == "your_openai_api_key_here":
                if self.environment == "production":
                    errors.append("Please set a real OPENAI_API_KEY in production")
                else:
                    warnings.append("Using placeholder API key - falling back to mock mode")
                    os.environ["USE_MOCK_TRANSCRIPTION"] = "true"
                    os.environ["USE_MOCK_SUMMARIZATION"] = "true"

        # Validate file size limits
        if self.max_audio_file_size_mb <= 0:
            errors.append("MAX_AUDIO_FILE_SIZE_MB must be positive")

        if self.max_audio_duration_seconds <= 0:
            errors.append("MAX_AUDIO_DURATION_SECONDS must be positive")

        # Validate rate limiting
        if self.rate_limit_per_minute <= 0:
            errors.append("RATE_LIMIT_PER_MINUTE must be positive")

        # Validate container-specific settings
        if self.database_connection_retries <= 0:
            errors.append("DATABASE_CONNECTION_RETRIES must be positive")

        if self.database_retry_delay_seconds <= 0:
            errors.append("DATABASE_RETRY_DELAY_SECONDS must be positive")

        # Log warnings
        for warning in warnings:
            logger.warning(f"Configuration warning: {warning}")

        # Raise errors if any
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(
                f"  - {error}" for error in errors
            )
            raise ConfigurationError(error_msg)

        logger.info("Configuration validation successful")
        self._log_configuration_summary()

    def _log_configuration_summary(self):
        """Log current configuration for debugging."""
        logger.info("=== VoiceForm Configuration ===")
        logger.info(f"Environment: {self.environment}")
        logger.info(f"Debug mode: {self.debug}")
        logger.info(f"Mock transcription: {self.use_mock_transcription}")
        logger.info(f"Mock summarization: {self.use_mock_summarization}")
        logger.info(f"OpenAI model: {self.openai_model}")
        logger.info(f"Max file size: {self.max_audio_file_size_mb}MB")
        logger.info(f"Max duration: {self.max_audio_duration_seconds}s")
        logger.info(f"Rate limit: {self.rate_limit_per_minute}/min")

        # Container-specific settings
        logger.info(f"DB connection retries: {self.database_connection_retries}")
        logger.info(f"DB retry delay: {self.database_retry_delay_seconds}s")
        logger.info(f"Container startup timeout: {self.container_startup_timeout_seconds}s")

        # Only log API key status, not the actual key
        if self.openai_api_key:
            key_preview = self.openai_api_key[:8] + "..." if len(self.openai_api_key) > 8 else "***"
            logger.info(f"OpenAI API key: {key_preview}")
        else:
            logger.info("OpenAI API key: Not configured")

        logger.info("==============================")


# Global configuration instance
config = Config()
