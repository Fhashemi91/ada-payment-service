from pydantic import BaseModel
from payment_service.models.payment import Status


class PaymentBase(BaseModel):
    order_id: int
    reference_id: int
    amount: int


class PaymentCreate(PaymentBase):
    pass


class Payment(PaymentBase):
    id: int
    user_id: int
    status: Status

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: str


class User(UserBase):
    id: int
    is_active: bool
    payments: list[Payment] = []

    class Config:
        orm_mode = True
