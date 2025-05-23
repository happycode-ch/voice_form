from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.transcription_repository import TranscriptionRepository
from app.schemas.transcription import TranscriptionSchema
from app.services.whisper_client import transcribe_audio

router = APIRouter()


@router.post("/", response_model=TranscriptionSchema)
async def transcribe_audio_file(
    file: UploadFile = File(...),
    qid: int = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Transcribe an audio file using Whisper and store in database.

    - file: The audio file to transcribe
    - qid: Question ID to associate with this transcription
    - language: Optional language code (en, de) to help transcription
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    if qid is None:
        raise HTTPException(status_code=400, detail="Question ID (qid) is required")

    try:
        # Get audio content
        audio_content = await file.read()

        # Call transcription service
        text = await transcribe_audio(audio_content, language)

        # Store transcription in database
        repo = TranscriptionRepository(db)
        transcription = repo.create(question_id=qid, text=text)

        return transcription

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
