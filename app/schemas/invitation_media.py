from pydantic import BaseModel
from typing import Optional

class InvitationMediaBase(BaseModel):
    file_url: str
    file_type: str
    label: Optional[str] = None # 'main_hero', 'church', 'gallery' և այլն

class InvitationMediaCreate(InvitationMediaBase):
    invitation_id: int

class InvitationMediaSchema(InvitationMediaBase):
    id: int
    invitation_id: int

    class Config:
        from_attributes = True