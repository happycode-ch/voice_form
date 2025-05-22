from sqlalchemy import Column, Integer, Text, DateTime, func
from app.db.models import Base

class Transcription(Base):
    __tablename__ = "transcriptions"
    id          = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, nullable=False)
    text        = Column(Text,    nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now()) 