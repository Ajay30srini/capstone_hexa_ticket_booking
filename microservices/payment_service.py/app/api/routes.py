from fastapi import APIRouter, Depends, HTTPException

from app.core.jwt import get_token, get_current_user_payload
from app.schemas.payment import PaymentConfirmIn
from app.services.payment_service import confirm_payment_and_booking

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/confirm")
async def confirm(payload: PaymentConfirmIn, _=Depends(get_current_user_payload), token: str = Depends(get_token)):
    try:
        return await confirm_payment_and_booking(token, payload.booking_id, payload.success)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))