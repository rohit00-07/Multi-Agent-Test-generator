from sqlalchemy import Column, String, Integer, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
import uuid
from datetime import datetime

class Test(Base):
    __tablename__ = "tests"

    test_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    level = Column(String)
    domains = Column(JSON)
    difficulty_mix = Column(JSON)
    total_questions = Column(Integer)

    questions = relationship("Question", back_populates="test")


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    test_id = Column(String, ForeignKey("tests.test_id"))
    domain = Column(String)
    difficulty = Column(String)
    question = Column(Text)
    options = Column(JSON)
    correct_option = Column(String)
    explanation = Column(Text)

    test = relationship("Test", back_populates="questions")