from sqlalchemy.orm import Session
from . import models, schemas


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
    return db.query(models.Shift).all()
