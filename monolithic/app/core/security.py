from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

print("✅ LOADED app/core/security.py (TRUNCATE FIX ACTIVE)")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

BCRYPT_MAX_BYTES = 72


def _truncate_to_72_bytes(password: str) -> str:
    b = password.encode("utf-8")
    if len(b) > BCRYPT_MAX_BYTES:
        b = b[:BCRYPT_MAX_BYTES]
    return b.decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    print("🔎 hash_password() bytes =", len(password.encode("utf-8")), "repr =", repr(password))
    safe = _truncate_to_72_bytes(password)
    print("✅ after truncate bytes =", len(safe.encode("utf-8")), "repr =", repr(safe))
    return pwd_context.hash(safe)


def verify_password(password: str, password_hash: str) -> bool:
    safe = _truncate_to_72_bytes(password)
    return pwd_context.verify(safe, password_hash)


def create_access_token(subject: str, extra: Optional[dict[str, Any]] = None) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }
    if extra:
        payload.update(extra)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)