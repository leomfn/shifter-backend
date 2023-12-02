from sqlalchemy.orm import Session
from . import models, schemas


def check_regular_signup_exists(
    db: Session, signup: schemas.CreateRegularSignup
) -> bool:
    signup_exists = (
        db.query(models.RegularSignup)
        .filter(
            models.RegularSignup.shift_id == signup.shift_id,
            models.RegularSignup.user_id == signup.user_id,
        )
        .first()
        != None
    )

    return signup_exists


def check_single_signout_exists(
    db: Session, signout: schemas.CreateSingleSignout
) -> bool:
    signout_exists = (
        db.query(models.SingleSignout)
        .filter(
            models.SingleSignout.shift_id == signout.shift_id,
            models.SingleSignout.user_id == signout.user_id,
        )
        .first()
        != None
    )

    return signout_exists


def check_single_signup_exists(db: Session, signup: schemas.CreateSingleSignup) -> bool:
    signup_exists = (
        db.query(models.SingleSignup)
        .filter(
            models.SingleSignup.shift_id == signup.shift_id,
            models.SingleSignup.user_id == signup.user_id,
        )
        .first()
        != None
    )

    return signup_exists
