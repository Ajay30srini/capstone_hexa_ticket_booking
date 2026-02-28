from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth_schema import RegisterIn, LoginIn, TokenOut
from app.schemas.user_schema import UserOut
from app.services.auth_service import register as register_user, login as login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    try:
        user, token = register_user(db, payload.email, payload.password, payload.role)
        return {"user": UserOut.model_validate(user), "access_token": token, "token_type": "bearer"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # TEMP debug so we see the real cause in Swagger
        db.rollback()
        raise HTTPException(status_code=400, detail=f"{type(e).__name__}: {e}")


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    try:
        token = login_user(db, payload.email, payload.password)
        return TokenOut(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))