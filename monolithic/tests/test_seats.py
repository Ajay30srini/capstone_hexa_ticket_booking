from datetime import datetime, timezone, timedelta
from tests.conftest import auth_header


def test_list_seats_for_event(client, organizer_token):
    create = client.post(
        "/events",
        json={
            "title": "Seat Event",
            "venue": "Chennai",
            "date": (datetime.now(timezone.utc) + timedelta(days=20)).isoformat(),
            "total_seats": 5,
        },
        headers=auth_header(organizer_token),
    )
    event_id = create.json()["id"]

    # publish so it behaves like real flows (optional for seats list)
    client.patch(f"/events/{event_id}/status", json={"status": "published"}, headers=auth_header(organizer_token))

    r = client.get(f"/events/{event_id}/seats")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["event_id"] == event_id
    assert data["total"] == 5
    assert len(data["seats"]) == 5