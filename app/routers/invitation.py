from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from app import schemas
from app.services.invitation import InvitationService
from app.services.rsvp import RSVPService
from app.dependencies import get_invitation_service, get_rsvp_service

router = APIRouter(prefix="/invite", tags=["Invitation & RSVP"])

# Jinja2 Templates-ի կարգավորում
templates = Jinja2Templates(directory="templates")


@router.get("/{slug}")
def get_invitation_page(
        slug: str,
        request: Request,
        service: InvitationService = Depends(get_invitation_service)
):
    """Բացում է կոնկրետ հրավիրատոմսի էջը"""
    invitation = service.get_invitation_data(slug)
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    # Որոշում ենք որ HTML տեմպլեյթն օգտագործենք
    template_file = f"designs/{invitation.template.html_file}"

    # Վերադարձնում ենք HTML-ը
    return templates.TemplateResponse(template_file, {
        "request": request,
        "invitation": invitation
    })


@router.post("/{slug}/rsvp")
def submit_rsvp_for_invitation(
        slug: str,
        rsvp_data: schemas.RSVPResponseBase,
        invitation_service: InvitationService = Depends(get_invitation_service),
        rsvp_service: RSVPService = Depends(get_rsvp_service)
):
    """Գրանցում է հյուրի պատասխանը տվյալ հրավիրատոմսի համար"""
    invitation = invitation_service.get_invitation_data(slug)
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    full_rsvp_data = schemas.RSVPResponseCreate(
        invitation_id=invitation.id,
        **rsvp_data.model_dump()
    )

    return rsvp_service.submit_response(full_rsvp_data)


# ... քո եղած ներմուծումները (imports) ...

@router.get("/{slug}/manage")
def get_admin_dashboard(
        slug: str,
        token: str,  # Ստանում ենք URL-ից՝ ?token=...
        request: Request,
        invitation_service: InvitationService = Depends(get_invitation_service),
        rsvp_service: RSVPService = Depends(get_rsvp_service)
):
    """Բացում է տվյալ հրավիրատոմսի կառավարման էջը (RSVP ցուցակը)"""
    invitation = invitation_service.get_invitation_data(slug)

    # Անվտանգության ստուգում (երբ հետագայում կավելացնես admin_token դաշտը)
    # if not invitation or invitation.admin_token != token:
    #     raise HTTPException(status_code=403, detail="Մուտքն արգելված է")

    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")

    # Ստանում ենք պատասխանները և վիճակագրությունը
    responses = rsvp_service.get_invitation_responses(invitation.id)
    stats = rsvp_service.get_invitation_stats(invitation.id)

    return templates.TemplateResponse("responses_dashboard.html", {
        "request": request,
        "invitation": invitation,
        "responses": responses,
        "stats": stats
    })