import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/tutor_service"
)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")
INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
CHUNK_SIZE = 500