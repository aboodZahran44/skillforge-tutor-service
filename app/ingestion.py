from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import CHUNK_SIZE, EMBEDDING_MODEL, OPENAI_API_KEY
from app.models import LessonChunk

_client = OpenAI(api_key=OPENAI_API_KEY)


def _split_into_chunks(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end].strip())
        start = end
    return [chunk for chunk in chunks if chunk]


def ingest_lesson(db: Session, lesson_id: int, course_id: int, content: str) -> int:
    chunks_text = _split_into_chunks(content)

    db.query(LessonChunk).filter(LessonChunk.lesson_id == lesson_id).delete()

    if not chunks_text:
        db.commit()
        return 0

    response = _client.embeddings.create(model=EMBEDDING_MODEL, input=chunks_text)
    vectors = [item.embedding for item in response.data]

    for order, (text, vector) in enumerate(zip(chunks_text, vectors, strict=True), start=1):
        db.add(
            LessonChunk(
                lesson_id=lesson_id,
                course_id=course_id,
                content=text,
                chunk_order=order,
                embedding=vector,
            )
        )

    db.commit()
    return len(chunks_text)