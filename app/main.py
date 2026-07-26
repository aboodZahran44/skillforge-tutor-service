from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth import get_tutor_scope, require_internal_api_key
from app.chat import stream_tutor_answer
from app.database import get_db
from app.ingestion import ingest_lesson
from app.retrieval import retrieve_relevant_chunks
from app.schemas import ChatRequest, LessonIngestRequest

app = FastAPI(title="SkillForge Tutor Service")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.post("/internal/lessons/ingest")
def ingest_lesson_endpoint(
    payload: LessonIngestRequest,
    db: Session = Depends(get_db),
    _: None = Depends(require_internal_api_key),
):
    chunks_created = ingest_lesson(db, payload.lesson_id, payload.course_id, payload.content)
    return {"chunks_created": chunks_created}


@app.post("/courses/{course_id}/chat")
def chat_with_tutor(
    course_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    scope: dict = Depends(get_tutor_scope),
):
    if scope["course_id"] != course_id:
        raise HTTPException(
            status_code=403,
            detail="This token is not scoped to the requested course.",
        )

    chunks = retrieve_relevant_chunks(db, course_id, payload.question)

    def event_stream():
        for piece in stream_tutor_answer(chunks, payload.question):
            yield f"data: {piece}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")