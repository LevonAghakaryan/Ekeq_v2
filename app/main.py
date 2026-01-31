from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.database import engine, Base  # Ներմուծում ենք engine-ը և Base-ը
from app.routers import home, catalog, invitation, admin

# IMPORT MODELS: Սա շատ կարևոր է։
# Մենք պետք է ներմուծենք բոլոր մոդելները, որպեսզի SQLAlchemy-ն տեսնի դրանք։
from app.models.category import Category
from app.models.template import Template
from app.models.invitation import Invitation
from app.models.invitation_media import InvitationMedia
from app.models.rsvp import RSVPResponse

# Ստեղծում ենք աղյուսակները բազայում (եթե գոյություն չունեն)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Invitation System")

# Ստատիկ ֆայլերի միացում
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ռութերների միացում
app.include_router(home.router)
app.include_router(catalog.router)
app.include_router(invitation.router)
app.include_router(admin.router)