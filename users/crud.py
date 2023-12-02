from sqlalchemy.orm import Session
from . import models, schemas
from auth import helpers as auth_helpers

def read_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def read_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def read_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.user_name == username).first()


def read_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = auth_helpers.fake_hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        user_name=user.user_name,
        member_status=user.member_status,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
