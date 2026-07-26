import os

from fastapi import Header, HTTPException
from jose import JWTError, jwt

from app.config import INTERNAL_API_KEY, JWT_SECRET_KEY

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "")


def get_tutor_scope(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header.")

    token = authorization.removeprefix("Bearer ")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    return {
        "user_id": payload["user_id"],
        "course_id": payload["course_id"],
        "enrollment_id": payload["enrollment_id"],
    }
    
def require_internal_api_key(x_internal_key: str = Header(...)):
    if x_internal_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid internal API key.")