from pydantic import BaseModel
from typing import Optional, TYPE_CHECKING
from datetime import datetime

# Սա IDE-ին ասում է, թե որտեղից գտնել InvitationSchema-ն
if TYPE_CHECKING:
    from .invitation import InvitationSchema

class OrderBase(BaseModel):
    customer_name: str
    phone_number: str
    preferred_contact: str
    template_id: int

class OrderCreate(OrderBase):
    pass

class OrderSchema(OrderBase):
    id: int
    status: str
    created_at: datetime

    # Պարտադիր չակերտների մեջ, որպեսզի runtime-ում սխալ չտա
    invitation: Optional["InvitationSchema"] = None

    class Config:
        from_attributes = True