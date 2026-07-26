from fastapi import FastAPI

app = FastAPI(title="SkillForge Tutor Service")


@app.get("/healthz")
def health_check():
    return {"status": "ok"}