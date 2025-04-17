from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter(
    prefix="/pages",
    tags=["pages"],
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def hotels(
        request: Request,
        hotels = Depends(get)):
    return templates.TemplateResponse(name="hotels.html",context= {"request": request})