from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time, Date
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)
    time_start = Column(Time)
    time_end = Column(Time)
    date_start = Column(Date)
    is_active = Column(Boolean)


class RegularSignup(Base):
    __tablename__ = "regular_signups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    date_start = Column(Date)
    date_end = Column(Date)


class SingleSignout(Base):
    __tablename__ = "single_signouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    signout_date = Column(Date)


class Signup(Base):
    __tablename__ = "signups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    type = Column(String)  # once, regular, ...
    date_once = Column(Date)
    date_start = Column(Date)
    date_end = Column(Date)
