from pydantic import BaseModel


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
