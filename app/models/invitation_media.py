from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class InvitationMedia(Base):
    __tablename__ = "invitation_media"

    id = Column(Integer, primary_key=True, index=True)
    invitation_id = Column(Integer, ForeignKey("invitations.id"), nullable=False)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(20), nullable=False)  # 'image' կամ 'video'

    invitation = relationship("Invitation", back_populates="media_files")