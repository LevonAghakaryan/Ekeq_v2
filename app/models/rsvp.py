from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class RSVPResponse(Base):
    __tablename__ = "rsvp_responses"

    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id"), nullable=False, index=True)
    guest_name = Column(String(200), nullable=False)
    # 'yes', 'no', 'maybe'
    attending = Column(String(10), nullable=False)
    guest_count = Column(Integer, default=1)
    message = Column(Text, nullable=True)
    submitted_at = Column(DateTime, server_default=func.now())

    invitation = relationship("Invitation", back_populates="responses")