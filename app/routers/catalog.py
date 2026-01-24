from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.services.template import TemplateService
from app.services.category import CategoryService
from app.dependencies import get_template_service, get_category_service

router = APIRouter(prefix="/catalog", tags=["Catalog"])
templates_html = Jinja2Templates(directory="templates")


@router.get("/")
def get_catalog(
        request: Request,
        category_id: int = None,
        t_service: TemplateService = Depends(get_template_service),
        c_service: CategoryService = Depends(get_category_service)
):
    # 1. Վերցնում ենք բոլոր կատեգորիաները վերևի ֆիլտրի համար
    categories = c_service.get_all_categories()

    # 2. Վերցնում ենք տեմպլեյթները (եթե category_id կա՝ ֆիլտրում ենք)
    if category_id:
        templates = t_service.get_templates_by_type(category_id)
    else:
        templates = t_service.get_full_catalog()

    # 3. Մատուցում ենք HTML-ը՝ փոխանցելով տվյալները
    return templates_html.TemplateResponse("catalog.html", {
        "request": request,
        "categories": categories,
        "templates": templates,
        "selected_category": category_id
    })