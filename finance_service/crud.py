from hashlib import sha1
from sqlalchemy.orm import Session

from finance_service.models.user import User
from finance_service.models.item_return import Return
from finance_service import schemas


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = sha1(user.password.encode("utf-8")).hexdigest()
    user = User(email=user.email, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_returns(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Return).offset(skip).limit(limit).all()


def register_return(db: Session, item: schemas.ReturnCreate, user_id: int):
    item = Return(**item.dict(), owner_id=user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
