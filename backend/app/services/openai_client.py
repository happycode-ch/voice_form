"""
File: backend/app/services/openai_client.py
Description: OpenAI GPT client for text summarization and analysis.
AI-hints:
- Exposes `async def summarize_text()` for response analysis
- Uses centralized configuration for API key and mock mode
- Returns structured analysis based on question type
- Handles rate limiting and API errors gracefully
"""
import json
from typing import Dict, Any, Tuple, Optional
import httpx
import logging
from app.config import config

logger = logging.getLogger(__name__)

class OpenAIError(Exception):
    """Raised when OpenAI API call fails."""
    pass

async def summarize_text(
    text: str, 
    question: str, 
    question_type: str = "open",
    language: Optional[str] = "en"
) -> Tuple[str, Dict[str, Any]]:
    """
    Summarize and analyze a text response using OpenAI's GPT.
    
    Args:
        text: The text to summarize (typically a transcription)
        question: The question that was asked
        question_type: Type of question (open, yes_no, likert)
        language: Optional language code for the output (en, de)
        
    Returns:
        Tuple containing:
        - summary: A concise summary of the response
        - analysis: Structured analysis of the response
        
    Raises:
        OpenAIError: If summarization fails
    """
    # Use mock summarization for development/testing if configured
    if config.use_mock_summarization:
        logger.info("Using mock summarization service")
        summary = "This is a mock summary for development purposes."
        analysis = {
            "sentiment": "neutral",
            "key_points": ["Mock point 1", "Mock point 2"],
            "confidence": 0.85
        }
        return summary, analysis

    if not config.openai_api_key:
        raise OpenAIError("OpenAI API key is required for summarization")

    # Build prompt based on question type
    system_prompt = _build_system_prompt(question_type, language)
    
    # Build user message
    user_message = f"""
Question: {question}
Response: {text}

Analyze the response according to the instructions.
"""
    
    # Prepare API request
    headers = {
        "Authorization": f"Bearer {config.openai_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.3,  # Lower temperature for more consistent outputs
        "response_format": {"type": "json_object"}
    }
    
    # Make API request
    try:
        logger.info(f"Calling OpenAI API with model: {config.openai_model}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=config.request_timeout_seconds
            )
            
            # Check for success and parse response
            if response.status_code == 200:
                response_data = response.json()
                content = response_data["choices"][0]["message"]["content"]
                
                # Parse the JSON response
                result = json.loads(content)
                
                # Extract summary and analysis
                summary = result.get("summary", "")
                analysis = result.get("analysis", {})
                
                logger.info(f"Summarization successful, summary length: {len(summary)} characters")
                return summary, analysis
            else:
                # Handle API error
                error_detail = response.json().get("error", {}).get("message", "Unknown error")
                logger.error(f"OpenAI API error (status {response.status_code}): {error_detail}")
                raise OpenAIError(f"API request failed: {error_detail}")
                
    except httpx.TimeoutException:
        logger.error("OpenAI API request timed out")
        raise OpenAIError("Request timed out")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI response as JSON: {e}")
        raise OpenAIError("Invalid response format from API")
    except Exception as e:
        logger.exception("Unexpected error in summarization service")
        raise OpenAIError(f"Summarization failed: {str(e)}")

def _build_system_prompt(question_type: str, language: str) -> str:
    """Build the system prompt based on question type and language."""
    base_prompt = """
You are an AI assistant that analyzes responses to structured questions.
Provide a concise summary and detailed analysis of the user's response.

Return your response as a JSON object with the following structure:
{
    "summary": "A concise 1-2 sentence summary of the response",
    "analysis": {
        // Analysis fields depending on question type
    }
}
"""
    
    if question_type == "yes_no":
        analysis_instructions = """
For yes/no questions, include in the analysis:
- "answer": The clear yes/no answer (or "unclear" if ambiguous)
- "confidence": A value from 0.0 to 1.0 indicating confidence in the answer
- "explanation": Brief explanation of the response
- "keywords": Array of important terms from the response
"""
    elif question_type == "likert":
        analysis_instructions = """
For Likert scale questions, include in the analysis:
- "rating": Numerical rating (1-5) extracted from the response
- "sentiment": One of ["very negative", "negative", "neutral", "positive", "very positive"]
- "key_factors": Array of factors mentioned that influenced the rating
- "confidence": A value from 0.0 to 1.0 indicating confidence in the rating extraction
"""
    else:  # open
        analysis_instructions = """
For open-ended questions, include in the analysis:
- "key_points": Array of 2-4 main points from the response
- "sentiment": Overall sentiment ("negative", "neutral", "positive", "mixed")
- "themes": Array of identified themes or topics
- "follow_up_areas": Optional array of potential follow-up question areas
"""
    
    # Add language instructions if German
    language_instructions = ""
    if language and language.lower() == "de":
        language_instructions = """
Provide all text output in German, including the summary and any text fields in the analysis.
"""
    
    return base_prompt + analysis_instructions + language_instructions 