from fastapi import FastAPI, Request
from app.config import settings
from app.proxy import forward

app = FastAPI(title="Ticket Booking Gateway", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.api_route("/auth/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def auth(path: str, request: Request):
    return await forward(request, f"{settings.AUTH_URL}/auth/{path}")

@app.api_route("/events/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def events(path: str, request: Request):
    return await forward(request, f"{settings.EVENT_URL}/events/{path}")

@app.api_route("/seat/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def seat(path: str, request: Request):
    return await forward(request, f"{settings.SEAT_URL}/seat/{path}")

@app.api_route("/bookings/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def bookings(path: str, request: Request):
    return await forward(request, f"{settings.BOOKING_URL}/bookings/{path}")

@app.api_route("/payments/{path:path}", methods=["GET","POST","PUT","PATCH","DELETE"])
async def payments(path: str, request: Request):
    return await forward(request, f"{settings.PAYMENT_URL}/payments/{path}")