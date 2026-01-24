from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    preferred_contact = Column(String(20), nullable=False)  # WhatsApp, Call, etc.
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    status = Column(String(20), default="New")  # New, In Progress, Completed
    created_at = Column(DateTime, server_default=func.now())

    # Կապերը
    template = relationship("Template", back_populates="orders")

    # Կապ դեպի Invitation (մեկ պատվերը ունենում է մեկ հրավիրատոմս)
    invitation = relationship("Invitation", back_populates="order", uselist=False)