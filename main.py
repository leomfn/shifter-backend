from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud, models, schemas, helpers
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# TODO: rethink this for prod environment
# https://fastapi.tiangolo.com/tutorial/cors/
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.read_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/shifts", response_model=schemas.Shift)
def create_shift(shift: schemas.Shift, db: Session = Depends(get_db)):
    return crud.create_shift(db=db, shift=shift)


@app.get("/shifts", response_model=list[schemas.ShiftResponse])
def read_all_shifts(db: Session = Depends(get_db)):
    return crud.read_shifts(db)


@app.get("/signups/single")
def get_all_single_signups(db: Session = Depends(get_db)):
    return crud.read_single_signups(db)


@app.post("/signups/single", status_code=status.HTTP_201_CREATED)
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


@app.delete("/signups/single/{signup_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.get("/signups/singlesignout")
def get_single_signouts_from_regular_signups(
    db: Session = Depends(get_db),
):
    return crud.read_single_signouts(db)


@app.post("/signups/singlesignout", status_code=status.HTTP_201_CREATED)
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


@app.delete(
    "/signups/singlesignout/{signout_id}", status_code=status.HTTP_204_NO_CONTENT
)
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


@app.get("/signups/regular")
def get_all_regular_signups(db: Session = Depends(get_db)):
    return crud.read_regular_signups(db)


@app.post("/signups/regular", status_code=status.HTTP_201_CREATED)
def sign_up_for_shift_regularly(
    signup: schemas.CreateRegularSignup, db: Session = Depends(get_db)
):
    if helpers.check_regular_signup_exists(db, signup):
        raise HTTPException(403, "Signup already exists")

    return crud.create_regular_signup(db=db, signup=signup)


@app.delete("/signups/regular/{signup_id}", status_code=status.HTTP_204_NO_CONTENT)
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
