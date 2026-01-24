from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    html_file = Column(String(100), nullable=False)
    price = Column(Float, default=0.0)
    image_url = Column(String(255), nullable=False)
    # Կապ կատեգորիայի հետ
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Relationship-ներ
    category = relationship("Category", back_populates="templates")
    invitations = relationship("Invitation", back_populates="template")
    orders = relationship("Order", back_populates="template")