from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING, Dict, Any
from datetime import datetime

if TYPE_CHECKING:
    from .invitation_media import InvitationMediaSchema
    from .rsvp import RSVPResponseSchema


# --- JSON-ի ներքին կառուցվածքի սխեմաները ---

class LocationSchema(BaseModel):
    type: str  # 'church', 'restaurant', 'bride_house'
    title: str
    address: str
    time: str
    map_url: Optional[str] = None


class InvitationContentSchema(BaseModel):
    couple_names: Dict[str, str]
    welcome_text: Dict[str, str]
    locations: List[LocationSchema]
    rsvp_settings: Optional[Dict[str, Any]] = None

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
    guest_token: Optional[str] = None
    event_date: Optional[datetime] = None
    content: Optional[InvitationContentSchema] = None

    # --- ՆՈՐ ԴԱՇՏԵՐ SPECIAL DESIGN-Ի ՀԱՄԱՐ ---
    is_custom: bool = False
    custom_html_path: Optional[str] = None


class InvitationCreate(InvitationBase):
    admin_token: Optional[str] = None


class InvitationSchema(InvitationBase):
    id: int
    created_at: datetime
    admin_token: str

    class Config:
        from_attributes = True


class InvitationFullSchema(InvitationSchema):
    media_files: List["InvitationMediaSchema"] = []
    responses: List["RSVPResponseSchema"] = []


class InvitationUpdateSchema(BaseModel):
    event_date: Optional[datetime] = None
    music_url: Optional[str] = None
    content: Optional[dict] = None
    # Ավելացված է թարմացման հնարավորություն
    is_custom: Optional[bool] = None
    custom_html_path: Optional[str] = None