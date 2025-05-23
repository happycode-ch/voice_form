"""
File: backend/app/repositories/transcription_repository.py
Description: Database operations for transcription data persistence.
AI-hints:
- Exposes create(question_id, text) -> Transcription
- Handles SQLAlchemy session lifecycle with commit/refresh
- Returns persisted object with auto-generated ID
"""
from sqlalchemy.orm import Session

from app.models.transcription import Transcription


class TranscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, question_id: int, text: str) -> Transcription:
        obj = Transcription(question_id=question_id, text=text)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
