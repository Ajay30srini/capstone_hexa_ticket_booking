from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.user_repository import get_user_by_email, create_user

ALLOWED_ROLES = {"customer", "organizer", "admin"}


def register(db: Session, email: str, password: str, role: str):
    role = role.strip().lower()

    if role not in ALLOWED_ROLES:
        raise ValueError(f"Invalid role. Allowed: {', '.join(sorted(ALLOWED_ROLES))}")

    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")

    user = create_user(
        db,
        email=email,
        password_hash=hash_password(password),
        role=role,
    )

    token = create_access_token(subject=str(user.id), extra={"role": user.role})
    return user, token


def login(db: Session, email: str, password: str) -> str:
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    return create_access_token(subject=str(user.id), extra={"role": user.role})