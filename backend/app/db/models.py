from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

class Questionnaire(Base):
    __tablename__ = "questionnaires"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    language = Column(String(2), default="en")  # en, de, etc.
    is_active = Column(Boolean, default=True)
    
    # Relationships
    questions = relationship("Question", back_populates="questionnaire", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="questionnaire")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    questionnaire_id = Column(String, ForeignKey("questionnaires.id"))
    text = Column(Text, nullable=False)
    type = Column(String, default="open")  # open, yes_no, likert, etc.
    order = Column(Integer, nullable=False)
    is_required = Column(Boolean, default=True)
    
    # Optional translations
    text_de = Column(Text)
    
    # Relationships
    questionnaire = relationship("Questionnaire", back_populates="questions")
    responses = relationship("Response", back_populates="question")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    questionnaire_id = Column(String, ForeignKey("questionnaires.id"))
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    is_expired = Column(Boolean, default=False)
    language = Column(String(2), default="en")
    
    # Privacy and retention
    auto_delete_at = Column(DateTime, nullable=True)
    is_data_retained = Column(Boolean, default=False)
    
    # Relationships
    questionnaire = relationship("Questionnaire", back_populates="sessions")
    responses = relationship("Response", back_populates="session", cascade="all, delete-orphan")

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("sessions.id"))
    question_id = Column(String, ForeignKey("questions.id"))
    audio_path = Column(String, nullable=True)  # Path to stored audio if retained
    transcription = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    analysis = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    session = relationship("Session", back_populates="responses")
    question = relationship("Question", back_populates="responses") 