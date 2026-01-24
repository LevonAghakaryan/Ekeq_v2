from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class RSVPResponseBase(BaseModel):
    guest_name: str
    attending: str # 'yes', 'no', 'maybe'
    guest_count: int = Field(default=1, ge=1) # Նվազագույնը 1 հոգի
    message: Optional[str] = None

class RSVPResponseCreate(RSVPResponseBase):
    invitation_id: int

class RSVPResponseSchema(RSVPResponseBase):
    id: int
    submitted_at: datetime

    class Config:
        from_attributes = True