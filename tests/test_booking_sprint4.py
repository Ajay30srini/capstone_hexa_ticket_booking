from datetime import datetime, timezone, timedelta
from tests.conftest import auth_header


def _create_published_event(client, organizer_token, total_seats=5):
    create = client.post(
        "/events",
        json={
            "title": "Booking Event",
            "venue": "Chennai",
            "date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "total_seats": total_seats,
        },
        headers=auth_header(organizer_token),
    )
    event_id = create.json()["id"]
    client.patch(f"/events/{event_id}/status", json={"status": "published"}, headers=auth_header(organizer_token))
    return event_id


def test_hold_then_confirm_payment(client, organizer_token, customer_token):
    event_id = _create_published_event(client, organizer_token, total_seats=3)

    hold = client.post(
        "/bookings",
        json={"event_id": event_id, "seat_numbers": ["S1", "S2"]},
        headers=auth_header(customer_token),
    )
    assert hold.status_code == 201, hold.text
    hold_data = hold.json()
    assert hold_data["status"] == "pending"
    booking_id = hold_data["id"]

    pay = client.post(
        "/payments/confirm",
        json={"booking_id": booking_id, "payment_reference": "PAY123"},
        headers=auth_header(customer_token),
    )
    assert pay.status_code == 200, pay.text
    assert pay.json()["status"] == "confirmed"

    seats = client.get(f"/events/{event_id}/seats").json()["seats"]
    s1 = next(s for s in seats if s["seat_number"] == "S1")
    s2 = next(s for s in seats if s["seat_number"] == "S2")
    assert s1["status"] == "booked"
    assert s2["status"] == "booked"


def test_cannot_hold_booked_seat(client, organizer_token, customer_token):
    event_id = _create_published_event(client, organizer_token, total_seats=2)

    hold1 = client.post("/bookings", json={"event_id": event_id, "seat_numbers": ["S1"]}, headers=auth_header(customer_token))
    booking_id = hold1.json()["id"]
    client.post("/payments/confirm", json={"booking_id": booking_id, "payment_reference": "PAYX"}, headers=auth_header(customer_token))

    hold2 = client.post("/bookings", json={"event_id": event_id, "seat_numbers": ["S1"]}, headers=auth_header(customer_token))
    assert hold2.status_code == 400


def test_cancel_releases_seats(client, organizer_token, customer_token):
    event_id = _create_published_event(client, organizer_token, total_seats=2)

    hold = client.post("/bookings", json={"event_id": event_id, "seat_numbers": ["S2"]}, headers=auth_header(customer_token))
    booking_id = hold.json()["id"]

    cancel = client.patch(f"/bookings/{booking_id}/cancel", headers=auth_header(customer_token))
    assert cancel.status_code == 200, cancel.text
    assert cancel.json()["status"] == "cancelled"

    seats = client.get(f"/events/{event_id}/seats").json()["seats"]
    s2 = next(s for s in seats if s["seat_number"] == "S2")
    assert s2["status"] == "available"