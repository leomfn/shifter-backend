from sqlalchemy import Column, Integer, ForeignKey, Date
from database import Base

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


class SingleSignup(Base):
    __tablename__ = "single_signups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    shift_id = Column(Integer, ForeignKey("shifts.id"))
    signup_date = Column(Date)
