from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_shift(db: Session, shift: schemas.Shift):
    new_shift = models.Shift(
        day_of_week=shift.day_of_week,
        time_start=shift.time_start,
        time_end=shift.time_end,
    )
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)
    return new_shift


def get_shift(db: Session, shift_id: int):
    return db.query(models.Shift).filter(models.Shift.id == shift_id).first()


def get_shifts(db: Session):
    return db.query(models.Shift).all()


def get_shift_signups(db: Session):
    return db.query(models.ShiftSignup).all()


def shift_signup(db: Session, user_id: int, shift_id: int):
    new_signup = models.ShiftSignup(user_id=user_id, shift_id=shift_id)
    db.add(new_signup)
    db.commit()
    db.refresh(new_signup)
    return new_signup


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
