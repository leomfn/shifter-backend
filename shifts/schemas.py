from pydantic import BaseModel
from datetime import time, date


class Shift(BaseModel):
    day_of_week: int
    time_start: time
    time_end: time
    date_start: date | None = None
    date_end: date | None = None
    is_active: bool = True


class ShiftResponse(Shift):
    id: int
