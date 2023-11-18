from sqlalchemy.orm import Session
import models, schemas
from datetime import date


def read_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def read_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def read_users(db: Session):
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


def read_shift_by_id(db: Session, shift_id: int):
    return db.query(models.Shift).filter(models.Shift.id == shift_id).first()


def read_shifts(db: Session):
    # TODO: sort shifts by day_of_week and time_start?
    return db.query(models.Shift).all()
    # signups = db.query(models.Shift).all()

    # print(shifts)

    # results = []

    # for shift in shifts:
    #     shift_data = {
    #         "shift_id": shift.id,
    #         "day_of_week": shift.day_of_week,
    #         "time_start": shift.time_start,
    #         "time_end": shift.time_end,
    #         "signups": [
    #             signup.user_id for signup in signups if signup.shift_id == shift.id
    #         ],
    #     }

    #     results.append(shift_data)

    # return results


def read_signups(db: Session):
    return db.query(models.Signup).all()


def check_shift_signup_exists(db: Session, signup: schemas.CreateSignup):
    signup_exists = (
        db.query(models.Signup)
        .filter(
            models.Signup.shift_id == signup.shift_id,
            models.Signup.user_id == signup.user_id,
            models.Signup.date_once == signup.date_once,
        )
        .first()
        != None
    )

    return signup_exists


def create_signup(db: Session, signup: schemas.SignupResponse):
    new_signup = models.Signup(
        user_id=signup.user_id,
        shift_id=signup.shift_id,
        type=signup.type,
        date_once=signup.date_once,
        date_start=signup.date_start,
        date_end=signup.date_end,
    )

    db.add(new_signup)
    db.commit()
    db.refresh(new_signup)
    return new_signup


# def create_date_signup(db: Session, user_id: int, shift_id: int, date: date):
#     print([user_id, shift_id, date])


def delete_signup(db: Session, signup_id: int):
    db.query(models.Signup).filter(models.Signup.id == signup_id).delete()
    db.commit()
