from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False) # հարսանիք, կնունք...
    image_url = Column(String(255), nullable=True)
    templates = relationship("Template", back_populates="category")