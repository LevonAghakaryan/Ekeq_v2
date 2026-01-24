from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Այս հատվածը լուծում է "Unresolved reference" խնդիրը
if TYPE_CHECKING:
    from .invitation_media import InvitationMediaSchema
    from .rsvp import RSVPResponseSchema

class InvitationBase(BaseModel):
    slug: str
    event_title: str
    template_id: int
    music_url: Optional[str] = None
    order_id: Optional[int] = None

class InvitationCreate(InvitationBase):
    pass

class InvitationSchema(InvitationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class InvitationFullSchema(InvitationSchema):
    # Չակերտները թույլ են տալիս Pydantic-ին սպասել մինչև բոլոր ֆայլերը բեռնվեն
    media_files: List["InvitationMediaSchema"] = []
    responses: List["RSVPResponseSchema"] = []