from hashlib import sha1
from sqlalchemy.orm import Session

from payment_service.models.user import User
from payment_service.models.payment import Payment, Status
from payment_service import schemas


def get_or_create(db: Session, model, **kwargs):
    instance = db.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()

    return instance


def get_payment(db: Session, payment_id: int, status: Status):
    return db.query(Payment).filter_by(id=payment_id, status=status).first()

def update_payment_status(db: Session, payment_id: int, status: Status):
    payment = db.query(Payment).filter_by(id=payment_id).first()
    if not payment:
        # FIXME
        raise Exception("payment not found!")

    payment.status = status
    db.add(payment)
    db.commit()

def get_payments(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(Payment).filter_by(user_id=user_id).offset(skip).limit(limit).all()


def register_payment(db: Session, info: schemas.PaymentCreate, user_id: int):
    user = get_or_create(db, User, id=user_id)

    payment = Payment(**info.dict(), status=Status.registered, user_id=user.id)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
