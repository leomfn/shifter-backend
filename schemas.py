from pydantic import BaseModel
from datetime import time, date


class Shift(BaseModel):
    day_of_week: int
    time_start: time
    time_end: time
    date_start: date | None = None
    date_end: date | None = None
    is_active: bool = True


class ShiftResponse(Shift):
    id: int


class CreateSignup(BaseModel):
    user_id: int
    shift_id: int
    type: str
    date_once: date | None = None
    date_start: date | None = None
    date_end: date | None = None


class SignupResponse(CreateSignup):
    id: int


class CreateRegularSignup(BaseModel):
    user_id: int
    shift_id: int
    date_start: date | None = None
    date_end: date | None = None


class RegularSignupResponse(CreateRegularSignup):
    id: int


class CreateSingleSignout(BaseModel):
    user_id: int
    shift_id: int
    signout_date: date | None = None


class SingleSignoutResponse(CreateSingleSignout):
    id: int


class CreateSingleSignup(BaseModel):
    user_id: int
    shift_id: int
    signup_date: date | None = None


class SingleSignupResponse(CreateSingleSignup):
    id: int


class UserBase(BaseModel):
    email: str
    user_name: str
    member_status: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
