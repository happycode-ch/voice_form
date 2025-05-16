from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.whisper_client import transcribe_audio
from app.db.session import get_db
from sqlalchemy.orm import Session
import uuid

router = APIRouter()

@router.post("/")
async def transcribe_audio_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    session_id: Optional[str] = None,
    language: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Transcribe an audio file using Whisper.
    
    - file: The audio file to transcribe
    - session_id: Optional session ID to associate with this transcription
    - language: Optional language code (en, de) to help transcription
    """
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    try:
        # Generate unique ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Get audio content
        audio_content = await file.read()
        
        # Call transcription service
        transcription = await transcribe_audio(audio_content, language)
        
        # TODO: Implement background task for storage if configured
        # background_tasks.add_task(store_transcription, transcription, session_id, db)
        
        return {
            "session_id": session_id,
            "transcription": transcription,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}") 