"""
File: backend/app/services/whisper_client.py
Description: Thin async wrapper around the OpenAI Whisper API for speech-to-text.
AI-hints:
- Exposes `async def transcribe_audio(path: Path) -> str`
- Wraps blocking I/O in `run_in_threadpool`
- Raises `WhisperError` on non-200 responses
- Uses centralized configuration for API key and mock mode
"""
import tempfile
import httpx
import io
import openai
from typing import Optional
import logging
from app.config import config

logger = logging.getLogger(__name__)

class WhisperError(Exception):
    """Raised when Whisper API call fails."""
    pass

async def transcribe_audio(audio_data: bytes, language: Optional[str] = None) -> str:
    """
    Transcribe audio data using OpenAI's Whisper API.
    
    Args:
        audio_data: Raw audio bytes
        language: Optional language code to help transcription (en, de)
        
    Returns:
        Transcribed text
        
    Raises:
        WhisperError: If transcription fails
    """
    # Use mock transcription for development/testing if configured
    if config.use_mock_transcription:
        logger.info("Using mock transcription service")
        return "This is a mock transcription for development purposes."
    
    # Check for API key only if not in mock mode
    if not config.openai_api_key:
        raise WhisperError("OpenAI API key is required for transcription")
    
    try:
        # Set OpenAI API key
        openai.api_key = config.openai_api_key
        
        # Create BytesIO object from audio data
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.wav"  # Set a name for the file
        
        # Prepare API call parameters
        params = {
            "model": "whisper-1",
            "file": audio_file,
            "timeout": config.request_timeout_seconds
        }
        
        if language:
            params["language"] = language
        
        logger.info(f"Calling Whisper API with language: {language or 'auto-detect'}")
        
        # Call the OpenAI API
        response = openai.audio.transcriptions.create(**params)
        
        # Return the transcribed text
        logger.info(f"Transcription successful, text length: {len(response.text)} characters")
        return response.text
                
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise WhisperError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error in transcription service: {str(e)}")
        raise WhisperError(f"Transcription failed: {str(e)}") 