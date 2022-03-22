from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from payment_service.database import Base
from sqlalchemy.orm import relationship
import enum


class Status(enum.Enum):
    registered = 0
    successful = 1
    cancelled = 2
    rejected = 3
    refund = 4


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    reference_id = Column(Integer)
    status = Column(Enum(Status))
    amount = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="payments")
