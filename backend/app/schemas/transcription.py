"""
File: backend/app/schemas/transcription.py
Description: Pydantic schema for transcription API responses.
AI-hints:
- Converts SQLAlchemy Transcription model to JSON via from_attributes
- Includes database ID for client-side tracking
- Auto-serializes datetime fields
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TranscriptionSchema(BaseModel):
    id: int
    question_id: int
    text: str
    created_at: datetime
    
    class Config:
        from_attributes = True 