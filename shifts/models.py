from sqlalchemy import Boolean, Column, Integer, Time, Date
from database import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)
    time_start = Column(Time)
    time_end = Column(Time)
    date_start = Column(Date)
    is_active = Column(Boolean)
