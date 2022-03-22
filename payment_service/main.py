from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from finance_service import crud, schemas
from finance_service.models.user import User
from finance_service.models.item_return import Return
from finance_service.database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@app.post("/users/{user_id}/return/", response_model=schemas.Return)
def register_return(
    user_id: int, item: schemas.ReturnCreate, db: Session = Depends(get_db)
):
    return crud.register_return(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Return])
def list_returns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_returns(db, skip=skip, limit=limit)
    return items
