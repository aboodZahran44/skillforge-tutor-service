from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class LessonChunk(Base):
    __tablename__ = "lesson_chunks"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False, index=True)
    content = Column(Text, nullable=False)
    chunk_order = Column(Integer, nullable=False)
    embedding = Column(Vector(1536), nullable=True)