from sqlalchemy import Boolean, Column, String, ForeignKey
from payment_service.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    payments = relationship("Payment", back_populates="user")
