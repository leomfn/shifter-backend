from sqlalchemy.orm import Session
import models, schemas


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
