from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .invitation_media import InvitationMediaSchema
    from .rsvp import RSVPResponseSchema

class InvitationBase(BaseModel):
    slug: str
    event_title: str
    template_id: int
    music_url: Optional[str] = None
    order_id: Optional[int] = None
    # Հյուրի տոկենը կարող է լինել բազային սխեմայում
    guest_token: Optional[str] = None

class InvitationCreate(InvitationBase):
    # Ստեղծելիս կարող ենք admin_token-ը չփոխանցել,
    # քանի որ Service-ը այն կգեներացնի ավտոմատ
    admin_token: Optional[str] = None

class InvitationSchema(InvitationBase):
    id: int
    created_at: datetime
    # Սա այն սխեման է, որը կպարունակի նաև ադմինի բանալին
    admin_token: str

    class Config:
        from_attributes = True

class InvitationFullSchema(InvitationSchema):
    # Ներառում է նաև մեդիա ֆայլերը և RSVP պատասխանները
    media_files: List["InvitationMediaSchema"] = []
    responses: List["RSVPResponseSchema"] = []