from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from finance_service.database import Base
from sqlalchemy.orm import relationship
import enum


class Status(enum.Enum):
    new = 1
    processing = 2
    rejected = 3
    accepted = 4
    refund = 5
    processed = 6


class Return(Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    reference_id = Column(Integer)
    status = Column(Enum(Status))

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="returns")
