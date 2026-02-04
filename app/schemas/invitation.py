from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING, Dict, Any
from datetime import datetime

if TYPE_CHECKING:
    from .invitation_media import InvitationMediaSchema
    from .rsvp import RSVPResponseSchema

# --- JSON-ի ներքին կառուցվածքի սխեմաները ---

class LocationSchema(BaseModel):
    type: str # 'church', 'restaurant', 'bride_house'
    title: str
    address: str
    time: str
    map_url: Optional[str] = None

class InvitationContentSchema(BaseModel):
    couple_names: Dict[str, str]
    welcome_text: Dict[str, str]
    locations: List[LocationSchema]
    rsvp_settings: Optional[Dict[str, Any]] = None

    # Ավելացնում ենք սա Swagger-ի համար 👇
    model_config = {
        "json_schema_extra": {
            "example": {
                "couple_names": {
                    "groom": "Արամ",
                    "bride": "Անի",
                    "separator": "&"
                },
                "welcome_text": {
                    "title": "Սիրելի Հյուրեր",
                    "description": "Սիրով հրավիրում ենք Ձեզ մեր հարսանյաց հանդեսին:"
                },
                "locations": [
                    {
                        "type": "church",
                        "title": "Պսակադրություն",
                        "address": "Սուրբ Գայանե եկեղեցի",
                        "time": "11:30",
                        "map_url": "https://goo.gl/maps/..."
                    }
                ],
                "rsvp_settings": {
                    "deadline": "2025-09-30",
                    "whatsapp_number": "37494000000"
                }
            }
        }
    }

class InvitationBase(BaseModel):
    slug: str
    event_title: str
    template_id: int
    music_url: Optional[str] = None
    order_id: Optional[int] = None
    # Հյուրի տոկենը կարող է լինել բազային սխեմայում
    guest_token: Optional[str] = None
    # Նոր դաշտերը
    event_date: Optional[datetime] = None
    content: Optional[InvitationContentSchema] = None # Մեր սահմանած JSON սխեման

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

class InvitationUpdateSchema(BaseModel):
    event_date: Optional[datetime] = None
    music_url: Optional[str] = None
    content: Optional[dict] = None