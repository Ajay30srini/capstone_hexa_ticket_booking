import httpx
from app.core.config import settings

async def ensure_event_is_published(event_id: int) -> None:
    url = f"{settings.EVENT_URL}/events/published"
    async with httpx.AsyncClient(timeout=20.0) as client:
        r = await client.get(url)
        r.raise_for_status()
        events = r.json()
        if not any(int(e["id"]) == int(event_id) for e in events):
            raise ValueError("Event not found or not published")