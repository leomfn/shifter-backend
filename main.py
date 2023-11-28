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


@app.get("/signups", response_model=list[schemas.SignupResponse])
def get_all_signups(db: Session = Depends(get_db)):
    return crud.read_signups(db)


@app.post("/signups")
def sign_up_for_shift(signup: schemas.CreateSignup, db: Session = Depends(get_db)):
    # Check if signup already exists
    if crud.check_shift_signup_exists(db, signup):
        raise HTTPException(403, "Signup already exists")

    if signup.type == "once":
        print("sign up one time")
    elif signup.type == "regular":
        print("sign up regular")
    else:
        print("unknown")

    return crud.create_signup(db, signup)


@app.delete("/signups/{id}")
def sign_out_from_shift(id: int, db: Session = Depends(get_db)):
    # if not crud.check_shift_signup_exists(db, signup):
    #     raise HTTPException(400, "Signup does not exist")

    # if signup.type == "once":
    #     print("sign out of one-time shift signup")

    return crud.delete_signup(db, signup_id=id)


@app.get("/signups/regular")
def get_all_regular_signups(db: Session = Depends(get_db)):
    return crud.read_regular_signups(db)


@app.post("/signups/regular")
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


# @app.post("/signups/toggle", response_model=schemas.ShiftSignup)
# def create_shift_signup(
#     signup_data: schemas.ShiftSignup, db: Session = Depends(get_db)
# ):
#     db_user = crud.read_user_by_id(db, user_id=signup_data.user_id)

#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     db_shift = crud.read_shift_by_id(db, shift_id=signup_data.shift_id)
#     if db_shift is None:
#         raise HTTPException(status_code=404, detail="Shift not found")

#     signup_exists = crud.check_shift_signup_exists(
#         db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
#     )
#     if signup_exists:
#         return crud.delete_signup(
#             db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
#         )
#     else:
#         return crud.create_signup(
#             db=db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
#         )
