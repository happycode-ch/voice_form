import os
import tempfile
import httpx
import io
import openai
from typing import Optional, Dict, Any
import base64
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Set OpenAI API key
openai.api_key = OPENAI_API_KEY
USE_MOCK = os.getenv("USE_MOCK_TRANSCRIPTION", "False").lower() == "true"

logger = logging.getLogger(__name__)

async def transcribe_audio(audio_data: bytes, language: Optional[str] = None) -> str:
    """
    Transcribe audio data using OpenAI's Whisper API.
    
    Args:
        audio_data: Raw audio bytes
        language: Optional language code to help transcription (en, de)
        
    Returns:
        Transcribed text
    """
    # Use mock transcription for development/testing if configured
    if USE_MOCK:
        logger.info("Using mock transcription service")
        return "This is a mock transcription for development purposes."
    
    # Check for API key only if not in mock mode
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is required for transcription")
    
    try:
        # Create BytesIO object from audio data
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.wav"  # Set a name for the file
        
        # Prepare API call parameters
        params = {
            "model": "whisper-1",
            "file": audio_file
        }
        
        if language:
            params["language"] = language
        
        # Call the OpenAI API
        response = openai.audio.transcriptions.create(**params)
        
        # Return the transcribed text
        return response.text
                
    except Exception as e:
        logger.exception(f"Error in transcription service: {str(e)}")
        raise 