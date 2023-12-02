from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String, unique=True)
    hashed_password = Column(String)
    member_status = Column(String)
    is_active = Column(Boolean, default=True)


