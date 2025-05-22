from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TranscriptionSchema(BaseModel):
    id: int
    question_id: int
    text: str
    created_at: datetime
    
    class Config:
        orm_mode = True 