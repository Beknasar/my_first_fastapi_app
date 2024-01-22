from fastapi import APIRouter, Request, Depends  # будет отдавать странички в формате html
from fastapi.templating import Jinja2Templates
from src.hotels.router import get_hotels_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=['Фронтенд']
)

templates = Jinja2Templates(directory="src/templates")

# очень важно в любом эндпоинте принимать request!
@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_hotels_by_location_and_time)
):
    # ответ в виде странички
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels},
    )