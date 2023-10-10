from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # items = relationship("Item", back_populates="owner")

class Shift(Base):
    __tablename__ = "shifts"
    
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)
    time_start = Column(Time)
    time_end = Column(Time)
    
class ShiftSignup(Base):
    __tablename__ = "signups"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
