from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    event_title = Column(String(200), nullable=False)

    # --- ՆՈՐ ԴԱՇՏԵՐ ---
    # Հարսանիքի հիմնական օրը (ֆիլտրման և օրացույցի համար)
    event_date = Column(DateTime, nullable=True)
    # Բոլոր դինամիկ տեքստերը (couple_names, welcome_text, locations, rsvp_settings)
    content = Column(JSON, nullable=True)
    # ------------------
    # Անվտանգության տոկեններ (UUID-ների համար)
    # guest_token-ը կարող է լինել nullable, եթե ուզում ես հանրային հրավիրատոմսեր ունենալ
    guest_token = Column(String(100), unique=True, nullable=True, index=True)

    # admin_token-ը պարտադիր է կառավարման էջի (Dashboard) համար
    admin_token = Column(String(100), unique=True, nullable=False, index=True)
    # Անհատական երաժշտություն (կամընտրական)
    music_url = Column(String(255), nullable=True)

    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)

    # Ավելացրինք order_id, որպեսզի հասկանանք՝ որ պատվերի արդյունքն է սա
    # nullable=True է, որպեսզի եթե ձեռքով (առանց պատվերի) հրավիրատոմս սարքես, խնդիր չլինի
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)

    created_at = Column(DateTime, server_default=func.now())

    # Կապերը
    template = relationship("Template", back_populates="invitations")
    responses = relationship("RSVPResponse", back_populates="invitation", cascade="all, delete-orphan")
    order = relationship("Order", back_populates="invitation")
    # Փոխված անունով կապը դեպի InvitationMedia
    media_files = relationship("InvitationMedia", back_populates="invitation", cascade="all, delete-orphan")