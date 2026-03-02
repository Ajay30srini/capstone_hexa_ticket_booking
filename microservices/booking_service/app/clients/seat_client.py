import httpx
from app.core.config import settings

def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

async def hold_seats(token: str, event_id: int, seat_numbers: list[str]) -> None:
    url = f"{settings.SEAT_URL}/seats/hold"
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, json={"event_id": event_id, "seat_numbers": seat_numbers}, headers=_auth_header(token))
        if r.status_code >= 400:
            raise ValueError(r.json().get("detail", "Seat hold failed"))

async def confirm_seats(token: str, event_id: int, seat_numbers: list[str]) -> None:
    url = f"{settings.SEAT_URL}/seats/confirm"
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, json={"event_id": event_id, "seat_numbers": seat_numbers}, headers=_auth_header(token))
        if r.status_code >= 400:
            raise ValueError(r.json().get("detail", "Seat confirm failed"))

async def release_seats(token: str, event_id: int, seat_numbers: list[str]) -> None:
    url = f"{settings.SEAT_URL}/seats/release"
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.post(url, json={"event_id": event_id, "seat_numbers": seat_numbers}, headers=_auth_header(token))
        if r.status_code >= 400:
            raise ValueError(r.json().get("detail", "Seat release failed"))