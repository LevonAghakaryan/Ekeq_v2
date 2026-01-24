from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.category import CategoryService
from app.dependencies import get_category_service


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def read_home(
        request: Request,
        service: CategoryService = Depends(get_category_service)
):
    # ՃԻՇՏ ԿԱՆՉԸ. քանի որ սերվիսը արդեն ունի repo, իսկ repo-ն՝ db-ն:
    categories = service.get_all_categories()

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "categories": categories
        }
    )