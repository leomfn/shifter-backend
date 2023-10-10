from pydantic import BaseModel
from datetime import time


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class Shift(BaseModel):
    day_of_week: int
    time_start: time
    time_end: time


class ShiftSignup(BaseModel):
    user_id: int
    shift_id: int


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    # items: list[Item] = []

    class Config:
        from_attributes = True
