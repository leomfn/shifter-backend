from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/shifts/", response_model=list[schemas.Shift])
def read_shifts(db: Session = Depends(get_db)):
    shifts = crud.get_shifts(db)
    return shifts


@app.post("/shifts/", response_model=schemas.Shift)
def create_shift(shift: schemas.Shift, db: Session = Depends(get_db)):
    return crud.create_shift(db=db, shift=shift)


@app.get("/shifts/signup/", response_model=list[schemas.ShiftSignup])
def read_shift_signups(db: Session = Depends(get_db)):
    shift_signups = crud.get_shift_signups(db)
    return shift_signups


@app.post("/shifts/signup/", response_model=schemas.ShiftSignup)
def create_shift_signup(
    signup_data: schemas.ShiftSignup, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=signup_data.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_shift = crud.get_shift(db, shift_id=signup_data.shift_id)
    if db_shift is None:
        raise HTTPException(status_code=404, detail="Shift not found")
    return crud.shift_signup(
        db=db, user_id=signup_data.user_id, shift_id=signup_data.shift_id
    )


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
