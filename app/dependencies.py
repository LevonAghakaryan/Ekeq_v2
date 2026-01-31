from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import get_db

# 1. Ներմուծում ենք Ռեպոզիտորիաները
from app.repositories.category import CategoryRepository
from app.repositories.template import TemplateRepository
from app.repositories.invitation import InvitationRepository
from app.repositories.rsvp import RSVPRepository
from app.repositories.order import OrderRepository
from app.repositories.invitation_media import InvitationMediaRepository # Ավելացված է

# 2. Ներմուծում ենք Սերվիսները
from app.services.category import CategoryService
from app.services.template import TemplateService
from app.services.invitation import InvitationService
from app.services.rsvp import RSVPService
from app.services.order import OrderService
from app.services.invitation_media import InvitationMediaService # Ավելացված է

# --- Dependency Functions ---

def get_category_service(db: Session = Depends(get_db)):
    repo = CategoryRepository(db)
    return CategoryService(repo)

def get_template_service(db: Session = Depends(get_db)):
    repo = TemplateRepository(db)
    return TemplateService(repo)

def get_invitation_service(db: Session = Depends(get_db)):
    repo = InvitationRepository(db)
    return InvitationService(repo)

def get_rsvp_service(db: Session = Depends(get_db)):
    repo = RSVPRepository(db)
    return RSVPService(repo)

def get_order_service(db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    return OrderService(repo)

# Սա այն ֆունկցիան էր, որը պակասում էր 👇
def get_invitation_media_service(db: Session = Depends(get_db)):
    repo = InvitationMediaRepository(db)
    return InvitationMediaService(repo)