from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import get_db
from . import schemas, crud
from auth import helpers as auth_helpers

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(auth_helpers.get_current_user)],
)


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.read_users(db)
    return users


@router.get("/me", response_model=schemas.User)
def get_current_user(user=Depends(auth_helpers.get_current_user)):
    return user


@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
