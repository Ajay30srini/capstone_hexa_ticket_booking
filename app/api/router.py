from fastapi import APIRouter
from app.api.routes.auth import router as auth_router

api_router = APIRouter()

@api_router.get("/health")
def health():
    return {"status": "ok"}

api_router.include_router(auth_router)