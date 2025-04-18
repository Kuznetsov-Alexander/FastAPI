from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import date

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.pages.router import router as router_pages
# from app.hotels.router import router as router_hotels
app = FastAPI()


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_pages)
# app.include_router(router_hotels)


class HotelsSearchArgs:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Optional[bool] = None,
                 stars: Optional[int] = Query(None, ge=1, le=5),
                 ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars

@app.get("/hotels/")
def get_hotels(
    search_args: HotelsSearchArgs = Depends()
):

    return search_args


