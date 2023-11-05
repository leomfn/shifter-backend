from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud, models, schemas
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


@app.get("/shifts", response_model=list[schemas.ShiftSignups])
def read_all_shifts(db: Session = Depends(get_db)):
    shift_signups = crud.read_shifts(db)
    return shift_signups


@app.post("/signups/toggle", response_model=schemas.ShiftSignup)
def create_shift_signup(
    signup_data: schemas.ShiftSignup, db: Session = Depends(get_db)
):
    db_user = crud.read_user_by_id(db, user_id=signup_data.user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_shift = crud.read_shift_by_id(db, shift_id=signup_data.shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")

    signup_exists = crud.check_shift_signup_exists(
        db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
    )
    if signup_exists:
        return crud.delete_signup(
            db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
        )
    else:
        return crud.create_signup(
            db=db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
        )
