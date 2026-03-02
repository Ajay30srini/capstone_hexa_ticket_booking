from app.clients.booking_client import confirm_booking

async def confirm_payment_and_booking(token: str, booking_id: int, success: bool) -> dict:
    if not success:
        return {"status": "failed", "booking_id": booking_id}

    booking = await confirm_booking(token, booking_id)
    return {"status": "paid", "booking": booking}