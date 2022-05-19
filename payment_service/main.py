from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from payment_service import crud, schemas
from payment_service.models.user import User
from payment_service.models.payment import Payment, Status
from payment_service.database import engine, Base, SessionLocal
from fastapi.responses import RedirectResponse, HTMLResponse
from payment_service.pubsub import submit_message

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/payments/{user_id}/payment", response_model=schemas.Payment)
def register_payment(
    user_id: str, info: schemas.PaymentCreate, db: Session = Depends(get_db)
):
    submit_message("payment register requested", user_id=str(user_id))
    return crud.register_payment(db=db, info=info, user_id=user_id)


@app.get("/payments/{user_id}", response_model=list[schemas.Payment])
def list_payment(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    submit_message("payment list requested", user_id=str(user_id))
    
    payments = crud.get_payments(db, user_id, skip=skip, limit=limit)
    return payments

@app.get("/pay/{payment_id}", response_class=HTMLResponse)
def pay(payment_id: int, db: Session = Depends(get_db)):
    payment = crud.get_payment(db=db, payment_id=payment_id, status=Status.registered)

    if not payment:
        return f"<center><h1>Invalid payment id {payment_id}</h1></center>"

    return f"""
    <html>
    <head>
    <link rel="stylesheet" href="https://unpkg.com/purecss@2.1.0/build/pure-min.css">
    </head>
    <body style="padding:20px;">
    <h1>Payment</h1>
    <p>You are going to pay {payment.amount} to our company</p>
    <form action="/pay/{payment.id}/success/">
      <input type="submit" value="Submit">
    </form>
    </body>
    </html>
    """

@app.get("/pay/{payment_id}/success", response_class=HTMLResponse)
def update_payments(payment_id: int, db: Session = Depends(get_db)):
    submit_message("payment update requested", payment_id=str(payment_id))
    
    payments = crud.update_payment_status(db, payment_id, Status.successful)
    return """<center><h1>Payment was successful</h1></center>"""
