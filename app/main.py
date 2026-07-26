from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_tutor_scope, require_internal_api_key
from app.database import get_db
from app.ingestion import ingest_lesson
from app.schemas import LessonIngestRequest

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


@app.get("/courses/{course_id}/ping")
def tutor_ping(course_id: int, scope: dict = Depends(get_tutor_scope)):
    if scope["course_id"] != course_id:
        raise HTTPException(
            status_code=403,
            detail="This token is not scoped to the requested course.",
        )

    return {"ok": True, "course_id": course_id, "user_id": scope["user_id"]}