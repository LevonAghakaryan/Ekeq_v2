from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core.config import settings
# Քո մաքուր import-ները services __init__-ից
from app import services, schemas
# Քո dependencies.py-ի ֆունկցիաները
from app.dependencies import (
    get_invitation_service,
    get_order_service,
    get_invitation_media_service,
    get_template_service
)

router = APIRouter(prefix="/system-admin", tags=["Super Admin"])
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

# 🔐 Մուտքի տվյալներն արդեն գալիս են .env-ից
ADMIN_USER = settings.admin_user
ADMIN_PASS = settings.admin_password

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Մուտքն արգելված է",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# --- Գլխավոր Dashboard ---

@router.get("/dashboard")
def super_admin_dashboard(
        request: Request,
        user: str = Depends(authenticate),
        invitation_service: services.InvitationService = Depends(get_invitation_service),
        order_service: services.OrderService = Depends(get_order_service),
        template_service: services.TemplateService = Depends(get_template_service)
):
    """Ցույց է տալիս բոլոր պատվերները և հասանելի դիզայնները"""
    orders = order_service.list_orders()
    templates_list = template_service.get_full_catalog()

    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "orders": orders,
        "templates": templates_list
    })


# --- Հրավիրատոմսի ստեղծում ---

@router.post("/invitations/create")
def admin_create_invitation(
        slug: str = Form(...),
        event_title: str = Form(...),
        template_id: int = Form(...),
        order_id: int = Form(None),
        user: str = Depends(authenticate),
        service: services.InvitationService = Depends(get_invitation_service)
):
    """Ստեղծում է նոր հրավիրատոմս (ավտոմատ գեներացնելով տոկենները)"""
    inv_data = schemas.InvitationCreate(
        slug=slug,
        event_title=event_title,
        template_id=template_id,
        order_id=order_id
    )
    service.create_invitation(inv_data)
    return RedirectResponse(url="/system-admin/dashboard", status_code=303)


# --- Մեդիա (URL-ների) ավելացում ---

@router.post("/media/add")
def admin_add_media(
        invitation_id: int = Form(...),
        file_url: str = Form(...),
        file_type: str = Form("image"),
        user: str = Depends(authenticate),
        service: services.InvitationMediaService = Depends(get_invitation_media_service)
):
    """Ավելացնում է նկարի կամ վիդեոյի URL տվյալ հրավիրատոմսին"""
    service.add_media_to_invitation(invitation_id, file_url, file_type)
    return RedirectResponse(url="/system-admin/dashboard", status_code=303)


# --- Պատվերի կարգավիճակի փոփոխություն ---

@router.post("/orders/{order_id}/complete")
def admin_complete_order(
        order_id: int,
        user: str = Depends(authenticate),
        service: services.OrderService = Depends(get_order_service)
):
    """Պատվերը նշում է որպես ավարտված"""
    service.complete_order(order_id)
    return RedirectResponse(url="/system-admin/dashboard", status_code=303)