from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from auth import helpers as auth_helpers
from . import schemas, crud

router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"],
    dependencies=[Depends(auth_helpers.get_current_user)],
)


@router.post("/", response_model=schemas.Shift)
def create_shift(shift: schemas.Shift, db: Session = Depends(get_db)):
    return crud.create_shift(db=db, shift=shift)


@router.get("/", response_model=list[schemas.ShiftResponse])
def read_all_shifts(db: Session = Depends(get_db)):
    return crud.read_shifts(db)
