from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from payment_service import crud, schemas
from payment_service.models.user import User
from payment_service.models.payment import Payment
from payment_service.database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/payments/{user_id}/payment/", response_model=schemas.Payment)
def register_payment(
    user_id: str, info: schemas.PaymentCreate, db: Session = Depends(get_db)
):
    return crud.register_payment(db=db, info=info, user_id=user_id)


@app.get("/payments/{user_id}", response_model=list[schemas.Payment])
def list_payment(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    payments = crud.get_payments(db, user_id, skip=skip, limit=limit)
    return payments
