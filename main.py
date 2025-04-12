from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from datetime import date

app = FastAPI()


@app.get("/hotels/")
def read_item(item_id: int,
              location: str,
              date_from: date,
              date_to: date,
              has_spa: Optional[bool] = None,
              stars: Optional[int] = Query(None, ge = 1, le = 5),
              ):
    return date_from, date_to

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date
@app.post("/bookings")
def add_booking(booking: SBooking):
    pass

