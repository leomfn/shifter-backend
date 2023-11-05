from sqlalchemy.orm import Session
import models, schemas


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
    shifts = db.query(models.Shift).all()
    signups = db.query(models.ShiftSignup).all()

    results = []

    for shift in shifts:
        shift_data = {
            "shift_id": shift.id,
            "day_of_week": shift.day_of_week,
            "time_start": shift.time_start,
            "time_end": shift.time_end,
            "signups": [
                signup.user_id for signup in signups if signup.shift_id == shift.id
            ],
        }

        results.append(shift_data)

    return results


def check_shift_signup_exists(db: Session, user_id: int, shift_id: int):
    signup_exists = (
        db.query(models.ShiftSignup)
        .filter(
            models.ShiftSignup.shift_id == shift_id,
            models.ShiftSignup.user_id == user_id,
        )
        .first()
        != None
    )

    return signup_exists


def create_signup(db: Session, user_id: int, shift_id: int):
    new_signup = models.ShiftSignup(user_id=user_id, shift_id=shift_id)
    # print("would create new shift signup ", {"user_id": user_id, "shift_id": shift_id})

    db.add(new_signup)
    db.commit()
    db.refresh(new_signup)
    return new_signup


def delete_signup(db: Session, user_id: int, shift_id: int):
    deleted_signup = models.ShiftSignup(user_id=user_id, shift_id=shift_id)
    db.query(models.ShiftSignup).filter(
        models.ShiftSignup.user_id == user_id, models.ShiftSignup.shift_id == shift_id
    ).delete()
    db.commit()
    return deleted_signup
