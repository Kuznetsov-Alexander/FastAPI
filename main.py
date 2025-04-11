from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(item_id: int, date_from, date_to):
    return item_id, date_from, date_to



