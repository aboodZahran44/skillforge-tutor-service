from pydantic import BaseModel


class LessonIngestRequest(BaseModel):
    lesson_id: int
    course_id: int
    content: str


class ChatRequest(BaseModel):
    question: str