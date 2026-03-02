from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.payment_schema import PaymentConfirmIn, PaymentConfirmOut
from app.services.payment_service import confirm_payment

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/confirm", response_model=PaymentConfirmOut)
def confirm(
    payload: PaymentConfirmIn,
    db: Session = Depends(get_db),
    user=Depends(require_roles("customer", "admin", "organizer")),
):
    try:
        booking = confirm_payment(db, payload.booking_id, payload.payment_reference)
        return PaymentConfirmOut(
            booking_id=booking.id,
            status=booking.status,
            message="Payment confirmed and booking completed",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))