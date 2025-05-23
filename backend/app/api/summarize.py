from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.openai_client import summarize_text

router = APIRouter()


class SummarizeRequest(BaseModel):
    text: str
    question: str
    question_type: str = "open"  # open, yes_no, likert
    session_id: Optional[str] = None
    language: Optional[str] = None


class SummarizeResponse(BaseModel):
    summary: str
    analysis: Dict
    question_id: Optional[str] = None


@router.post("/", response_model=SummarizeResponse)
async def summarize_response(data: SummarizeRequest, db: Session = Depends(get_db)):
    """
    Summarize and analyze a text response based on the question context.

    - text: The text to summarize (typically a transcription)
    - question: The question that was asked
    - question_type: Type of question (open, yes_no, likert)
    - session_id: Optional session ID to associate with this analysis
    - language: Optional language for the summary output
    """
    try:
        # Call summarization service
        summary, analysis = await summarize_text(
            text=data.text,
            question=data.question,
            question_type=data.question_type,
            language=data.language,
        )

        # TODO: Store summary in database if session_id is provided

        return SummarizeResponse(
            summary=summary, analysis=analysis, question_id=data.session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")


@router.post("/batch")
async def batch_summarize(
    responses: List[SummarizeRequest],
    language: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Process multiple responses in a batch."""
    try:
        results = []
        for response in responses:
            # Override language if provided at batch level
            if language:
                response.language = language

            summary, analysis = await summarize_text(
                text=response.text,
                question=response.question,
                question_type=response.question_type,
                language=response.language,
            )

            results.append(
                {
                    "summary": summary,
                    "analysis": analysis,
                    "question_id": response.session_id,
                }
            )

        return {"results": results}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Batch summarization failed: {str(e)}"
        )
