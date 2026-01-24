from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.services.invitation import InvitationService
from app.services.rsvp import RSVPService
from app.dependencies import get_invitation_service, get_rsvp_service

router = APIRouter(prefix="/invite", tags=["Invitation & RSVP"])


@router.get("/{slug}")
def get_invitation_page(
        slug: str,
        service: InvitationService = Depends(get_invitation_service)
):
    """Բացում է կոնկրետ հրավիրատոմսի էջը"""
    invitation = service.get_invitation_data(slug)
    if not invitation:
        raise HTTPException(status_code=404, detail="Հրավիրատոմսը չի գտնվել")
    return invitation


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