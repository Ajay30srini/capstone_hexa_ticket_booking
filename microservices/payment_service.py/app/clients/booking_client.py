import httpx
from app.core.config import settings

def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

async def confirm_booking(token: str, booking_id: int) -> dict:
    url = f"{settings.BOOKING_URL}/bookings/{booking_id}/confirm"
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, headers=_auth_header(token))
        if r.status_code >= 400:
            raise ValueError(r.json().get("detail", "Booking confirm failed"))
        return r.json()