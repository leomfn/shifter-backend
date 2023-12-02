from sqlalchemy.orm import Session
from . import models, schemas


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


def delete_signup(db: Session, signup_id: int):
    db.query(models.Signup).filter(models.Signup.id == signup_id).delete()
    db.commit()


# Regular Signups CRUD
def create_regular_signup(
    db: Session, signup: schemas.CreateRegularSignup
) -> schemas.RegularSignupResponse:
    new_regular_signup = models.RegularSignup(
        user_id=signup.user_id,
        shift_id=signup.shift_id,
        date_start=signup.date_start,
        date_end=signup.date_end,
    )

    db.add(new_regular_signup)
    db.commit()
    db.refresh(new_regular_signup)
    return new_regular_signup


def read_regular_signups(db: Session) -> list[schemas.RegularSignupResponse]:
    return db.query(models.RegularSignup).all()


def read_regular_signup_by_id(
    db: Session, signup_id: int
) -> schemas.RegularSignupResponse | None:
    return (
        db.query(models.RegularSignup)
        .filter(models.RegularSignup.id == signup_id)
        .one_or_none()
    )


# Single Signouts CRUD
def read_single_signouts(db: Session) -> list[schemas.SingleSignoutResponse]:
    return db.query(models.SingleSignout).all()


# Single Signups CRUD
def read_single_signups(db: Session) -> list[schemas.SingleSignupResponse]:
    return db.query(models.SingleSignup).all()
