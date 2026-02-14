from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean  # Ավելացրել ենք Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    event_title = Column(String(200), nullable=False)

    # --- ՆՈՐ ԴԱՇՏԵՐ ---
    event_date = Column(DateTime, nullable=True)
    content = Column(JSON, nullable=True)

    # Անվտանգության տոկեններ
    guest_token = Column(String(100), unique=True, nullable=True, index=True)
    admin_token = Column(String(100), unique=True, nullable=False, index=True)

    # Անհատական երաժշտություն
    music_url = Column(String(255), nullable=True)

    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True, index=True)

    # ============================================================
    # 👇 ԱՎԵԼԱՑՐՈՒ ԱՅՍ ԵՐԿՈՒ ՏՈՂԸ SPECIAL DESIGN-Ի ՀԱՄԱՐ 👇
    is_custom = Column(Boolean, default=False)  # Նշում է՝ արդյոք սա հատուկ դիզայն է
    custom_html_path = Column(String(255), nullable=True)  # HTML ֆայլի անունը/ճանապարհը
    # ============================================================

    created_at = Column(DateTime, server_default=func.now())

    # Կապերը
    template = relationship("Template", back_populates="invitations")
    responses = relationship("RSVPResponse", back_populates="invitation", cascade="all, delete-orphan")
    order = relationship("Order", back_populates="invitation")
    media_files = relationship("InvitationMedia", back_populates="invitation", cascade="all, delete-orphan")