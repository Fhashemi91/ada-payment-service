from pydantic import BaseModel
from finance_service.models.item_return import Status


class ReturnBase(BaseModel):
    order_id: int
    reference_id = int
    status: Status

class ReturnCreate(ReturnBase):
    pass

class Return(ReturnBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Return] = []

    class Config:
        orm_mode = True
