from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app import schemas
from app.services.invitation import InvitationService
from app.services.rsvp import RSVPService
from app.dependencies import get_invitation_service, get_rsvp_service
from datetime import timedelta
router = APIRouter(prefix="/invite", tags=["Invitation & RSVP"])

# Jinja2 Templates-ի կարգավորում
templates = Jinja2Templates(directory="templates")


@router.get("/{slug}")
def get_invitation_page(
        slug: str,
        request: Request,
        gt: str = None,
        service: InvitationService = Depends(get_invitation_service)
):
    invitation = service.get_invitation_data(slug)

    # 1. 🔐 Անվտանգության ստուգում
    if invitation.guest_token:
        if invitation.guest_token != gt:
            raise HTTPException(status_code=403)

    # 2. 🎨 Դիզայնի ընտրություն (ՊԵՏՔ Է ԼԻՆԻ IF-ԻՑ ԴՈՒՐՍ)
    # Սա կաշխատի թե՛ Public, թե՛ Private հրավիրատոմսերի համար
    if getattr(invitation, 'is_custom', False) and invitation.custom_html_path:
        template_file = invitation.custom_html_path
    else:
        template_file = f"designs/{invitation.template.html_file}"

    return templates.TemplateResponse(template_file, {
        "request": request,
        "invitation": invitation,
        "timedelta": timedelta
    })


@router.get("/{slug}/manage")
def get_admin_dashboard(
        slug: str,
        at: str,  # Ադմինի տոկենը URL-ից (?at=...)
        request: Request,
        invitation_service: InvitationService = Depends(get_invitation_service),
        rsvp_service: RSVPService = Depends(get_rsvp_service)
):
    """Բացում է տվյալ հրավիրատոմսի կառավարման էջը (Dashboard)"""
    invitation = invitation_service.get_invitation_data(slug)

    # 🔐 Պարտադիր անվտանգության ստուգում ադմինի համար
    # Առանց ճիշտ ADMIN_TOKEN-ի ոչ ոք չի կարող տեսնել հյուրերի ցանկը
    if not invitation or invitation.admin_token != at:
        raise HTTPException(
            status_code=403,
            detail="Մուտքն արգելված է: Սխալ կառավարման կոդ:"
        )

    # Ստանում ենք պատասխանները և վիճակագրությունը
    responses = rsvp_service.get_invitation_responses(invitation.id)
    stats = rsvp_service.get_invitation_stats(invitation.id)

    return templates.TemplateResponse("responses_dashboard.html", {
        "request": request,
        "invitation": invitation,
        "responses": responses,
        "stats": stats
    })


@router.post("/{slug}/rsvp")
def submit_rsvp_for_invitation(
        slug: str,
        rsvp_data: schemas.RSVPResponseBase,
        invitation_service: InvitationService = Depends(get_invitation_service),
        rsvp_service: RSVPService = Depends(get_rsvp_service)
):
    """Գրանցում է հյուրի պատասխանը"""
    invitation = invitation_service.get_invitation_data(slug)

    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    # Ստեղծում ենք լիարժեք RSVP օբյեկտ՝ կապելով հրավիրատոմսի ID-ի հետ
    full_rsvp_data = schemas.RSVPResponseCreate(
        invitation_id=invitation.id,
        **rsvp_data.model_dump()
    )

    return rsvp_service.submit_response(full_rsvp_data)

@router.post("/create", response_model=schemas.InvitationSchema)
def create_new_invitation(
    invitation_data: schemas.InvitationCreate,
    service: InvitationService = Depends(get_invitation_service)
):
    # Այստեղ սերվիսը կգեներացնի տոկենները և կպահի բազայում
    new_invitation = service.create_invitation(invitation_data)
    return new_invitation