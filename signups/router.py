from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import helpers as auth_helpers
from . import models, schemas, crud, helpers

router = APIRouter(
    prefix="/signups",
    tags=["Signups"],
    dependencies=[Depends(auth_helpers.get_current_user)],
)


@router.get("/single")
def get_all_single_signups(db: Session = Depends(get_db)):
    return crud.read_single_signups(db)


@router.post("/single", status_code=status.HTTP_201_CREATED)
def create_single_signup(
    signup: schemas.CreateSingleSignup, db: Session = Depends(get_db)
) -> schemas.SingleSignupResponse:
    if helpers.check_single_signout_exists(db, signup):
        raise HTTPException(403, "Signup already exists")

    new_signup = models.SingleSignup(
        user_id=signup.user_id,
        shift_id=signup.shift_id,
        signup_date=signup.signup_date,
    )

    db.add(new_signup)
    db.commit()
    db.refresh(new_signup)
    return new_signup


@router.delete("/single/{signup_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_signup(signup_id: int, db: Session = Depends(get_db)):
    num_rows_deleted = (
        db.query(models.SingleSignup)
        .filter(
            models.SingleSignup.id == signup_id,
        )
        .delete()
    )

    if num_rows_deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    elif num_rows_deleted > 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot delete more than one record",
        )
    else:
        db.commit()


@router.get("/singlesignout")
def get_single_signouts_from_regular_signups(
    db: Session = Depends(get_db),
):
    return crud.read_single_signouts(db)


@router.post("/singlesignout", status_code=status.HTTP_201_CREATED)
def create_single_signout_for_regular_signup(
    signout: schemas.CreateSingleSignout, db: Session = Depends(get_db)
) -> schemas.SingleSignoutResponse:
    if helpers.check_single_signout_exists(db, signout):
        raise HTTPException(403, "Signout already exists")

    new_single_signout = models.SingleSignout(
        user_id=signout.user_id,
        shift_id=signout.shift_id,
        signout_date=signout.signout_date,
    )

    db.add(new_single_signout)
    db.commit()
    db.refresh(new_single_signout)
    return new_single_signout


@router.delete("/singlesignout/{signout_id}", status_code=status.HTTP_204_NO_CONTENT)
def sign_back_in_to_regular_shift(signout_id: int, db: Session = Depends(get_db)):
    num_rows_deleted = (
        db.query(models.SingleSignout)
        .filter(
            models.SingleSignout.id == signout_id,
        )
        .delete()
    )

    if num_rows_deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    elif num_rows_deleted > 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot delete more than one record",
        )
    else:
        db.commit()


@router.get("/regular")
def get_all_regular_signups(db: Session = Depends(get_db)):
    return crud.read_regular_signups(db)


@router.post("/regular", status_code=status.HTTP_201_CREATED)
def sign_up_for_shift_regularly(
    signup: schemas.CreateRegularSignup, db: Session = Depends(get_db)
):
    if helpers.check_regular_signup_exists(db, signup):
        raise HTTPException(403, "Signup already exists")

    return crud.create_regular_signup(db=db, signup=signup)


@router.delete("/regular/{signup_id}", status_code=status.HTTP_204_NO_CONTENT)
def sign_out_from_regular_shift(signup_id: int, db: Session = Depends(get_db)):
    num_rows_deleted = (
        db.query(models.RegularSignup)
        .filter(
            models.RegularSignup.id == signup_id,
        )
        .delete()
    )

    if num_rows_deleted == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found"
        )
    elif num_rows_deleted > 1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot delete more than one record",
        )
    else:
        db.commit()
