from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from core.config import settings
import json
from app import services, schemas
from app.dependencies import (
    get_invitation_service,
    get_order_service,
    get_invitation_media_service,
    get_template_service,
    get_rsvp_service
)

router = APIRouter(prefix="/system-admin", tags=["Super Admin"])
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

# 🔐 Աուդենտիֆիկացիա
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
        order_service: services.OrderService = Depends(get_order_service),
        template_service: services.TemplateService = Depends(get_template_service)
):
    orders = order_service.list_orders()
    all_templates = template_service.get_full_catalog()

    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "orders": orders,
        "templates": all_templates
    })


# --- Հրավիրատոմսի Ստեղծում ---
@router.post("/invitations/create")
def admin_create_invitation(
        order_id: int = Form(...),
        template_id: int = Form(...),
        slug: str = Form(...),
        event_title: str = Form(...),
        content_json: str = Form(...),
        user: str = Depends(authenticate),
        invitation_service: services.InvitationService = Depends(get_invitation_service),
        order_service: services.OrderService = Depends(get_order_service)
):
    try:
        # Փորձում ենք վերածել տեքստը JSON-ի
        content_data = json.loads(content_json)

        invitation_data = schemas.InvitationCreate(
            slug=slug,
            event_title=event_title,
            template_id=template_id,
            order_id=order_id,
            content=content_data
        )

        invitation_service.create_invitation(invitation_data)

        # Պատվերի կարգավիճակը դարձնում ենք "In Progress" կամ "Completed"
        order_service.repo.update_status(order_id, "Completed")

        return RedirectResponse(url="/system-admin/dashboard?success=created", status_code=303)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Սխալ JSON ֆորմատ")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Մեդիա ֆայլերի ավելացում ---
@router.post("/invitations/{invitation_id}/media")
def admin_add_media(
        invitation_id: int,
        file_url: str = Form(...),
        file_type: str = Form("image"),
        label: str = Form(None),
        user: str = Depends(authenticate),
        media_service: services.InvitationMediaService = Depends(get_invitation_media_service)
):
    media_service.add_media_to_invitation(
        invitation_id=invitation_id,
        file_url=file_url,
        file_type=file_type,
        label=label
    )
    return RedirectResponse(url="/system-admin/dashboard?success=media_added", status_code=303)


# --- Պատվերի կարգավիճակի փոփոխություն ---
@router.post("/orders/{order_id}/status")
def admin_update_order_status(
        order_id: int,
        status: str = Form(...),
        user: str = Depends(authenticate),
        order_service: services.OrderService = Depends(get_order_service)
):
    order_service.repo.update_status(order_id, status)
    return RedirectResponse(url="/system-admin/dashboard", status_code=303)


# --- Հրավիրատոմսի Տեքստերի Թարմացում ---
@router.post("/invitations/update-by-token")
def admin_update_content_by_token(
        admin_token: str = Form(...),
        event_date: str = Form(None),
        music_url: str = Form(None),
        content_json: str = Form(...),
        user: str = Depends(authenticate),
        service: services.InvitationService = Depends(get_invitation_service)
):
    try:
        update_data = {
            "content": json.loads(content_json),
            "music_url": music_url,
            "event_date": event_date  # Այստեղ կախված է ֆորմատից, կարող է պետք լինել դարձնել datetime
        }
        service.update_invitation_by_token(admin_token, update_data)
        return RedirectResponse(url="/system-admin/dashboard", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Թարմացման սխալ")