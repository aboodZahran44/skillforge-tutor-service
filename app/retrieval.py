from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import EMBEDDING_MODEL, OPENAI_API_KEY
from app.models import LessonChunk

_client = OpenAI(api_key=OPENAI_API_KEY)


def retrieve_relevant_chunks(db: Session, course_id: int, question: str, top_k: int = 3):
    response = _client.embeddings.create(model=EMBEDDING_MODEL, input=[question])
    question_vector = response.data[0].embedding

    stmt = (
        select(LessonChunk)
        .where(LessonChunk.course_id == course_id)
        .order_by(LessonChunk.embedding.l2_distance(question_vector))
        .limit(top_k)
    )
    return list(db.scalars(stmt))