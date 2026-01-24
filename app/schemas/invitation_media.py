from pydantic import BaseModel

class InvitationMediaBase(BaseModel):
    file_url: str
    file_type: str

class InvitationMediaCreate(InvitationMediaBase):
    invitation_id: int

class InvitationMediaSchema(InvitationMediaBase):
    id: int
    invitation_id: int

    class Config:
        from_attributes = True