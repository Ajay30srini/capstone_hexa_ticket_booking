from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_token
from app.repos.user_repo import get_user_by_id
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, MeOut
from app.services.auth_service import register as register_user, login as login_user

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=TokenOut, status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    try:
        _, token = register_user(db, payload.email, payload.password, payload.role)
        return TokenOut(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    try:
        token = login_user(db, payload.email, payload.password)
        return TokenOut(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=MeOut)
def me(
    db: Session = Depends(get_db),
    creds: HTTPAuthorizationCredentials = Depends(bearer),
):
    try:
        payload = decode_token(creds.credentials)
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = get_user_by_id(db, int(sub))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")