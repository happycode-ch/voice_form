import os
import tempfile
import httpx
from typing import Optional, Dict, Any
import base64
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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
    
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is required for transcription")
    
    # Create a temporary file for the audio data
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(audio_data)
        temp_audio_path = temp_audio.name
    
    try:
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Prepare form data with optional language parameter
        form_data = {
            "model": "whisper-1",
            "response_format": "text"
        }
        
        if language:
            form_data["language"] = language
        
        # Open the temporary file for API upload
        files = {
            "file": ("audio.wav", open(temp_audio_path, "rb"), "audio/wav")
        }
        
        # Make API request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers,
                data=form_data,
                files=files,
                timeout=30.0  # Longer timeout for audio processing
            )
            
            # Check for success and return transcription
            if response.status_code == 200:
                # For text response format, the response is just the text
                return response.text.strip()
            else:
                # Handle API error
                error_detail = response.json().get("error", {}).get("message", "Unknown error")
                logger.error(f"Transcription API error: {error_detail}")
                raise Exception(f"Transcription failed: {error_detail}")
                
    except Exception as e:
        logger.exception("Error in transcription service")
        raise
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path) 