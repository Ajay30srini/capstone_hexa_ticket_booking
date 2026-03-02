from fastapi import APIRouter
from app.api.routes.seats import router as seats_router

from app.api.routes.auth import router as auth_router
from app.api.routes.events import router as events_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.payments import router as payments_router
api_router = APIRouter()

@api_router.get("/health")
def health():
    return {"status": "ok"}

api_router.include_router(auth_router)
api_router.include_router(events_router)
api_router.include_router(bookings_router)
api_router.include_router(seats_router)
api_router.include_router(payments_router)