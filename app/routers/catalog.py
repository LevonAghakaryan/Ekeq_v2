from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.services.template import TemplateService
from app.services.category import CategoryService
from app.services.order import OrderService
from app.dependencies import get_template_service, get_category_service, get_order_service
from app.schemas import OrderCreate

router = APIRouter(prefix="/catalog", tags=["Catalog"])
templates_html = Jinja2Templates(directory="templates")


@router.get("/")
def get_catalog(
        request: Request,
        category_id: int = None,
        t_service: TemplateService = Depends(get_template_service),
        c_service: CategoryService = Depends(get_category_service)
):
    categories = c_service.get_all_categories()

    if category_id:
        templates = t_service.get_templates_by_type(category_id)
    else:
        templates = t_service.get_full_catalog()

    return templates_html.TemplateResponse("catalog.html", {
        "request": request,
        "categories": categories,
        "templates": templates,
        "selected_category": category_id
    })


# --- Ավելացված POST ֆունկցիան ---
@router.post("/order")
async def create_order(
        customer_name: str = Form(...),
        phone_number: str = Form(...),
        preferred_contact: str = Form(...),
        template_id: int = Form(...),
        o_service: OrderService = Depends(get_order_service)
):
    try:
        # 1. Ձեռքով սարքում ենք Schema-ն եկած Form տվյալներից
        order_data = OrderCreate(
            customer_name=customer_name,
            phone_number=phone_number,
            preferred_contact=preferred_contact,
            template_id=template_id
        )

        # 2. Փոխանցում ենք Service-ին, որը կգրանցի բազայում
        o_service.place_order(order_data)

        # 3. Վերադարձնում ենք հաջողության պատասխան (AJAX-ի համար)
        return JSONResponse(content={"status": "success", "message": "Պատվերն ընդունված է"}, status_code=201)

    except Exception as e:
        # Սխալի դեպքում ուղարկում ենք մանրամասները
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=400)