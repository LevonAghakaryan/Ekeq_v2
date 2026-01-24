from pydantic import BaseModel
from typing import Optional


class TemplateBase(BaseModel):
    name: str
    html_file: str
    price: float
    image_url: str
    category_id: int


class TemplateCreate(TemplateBase):
    pass


class TemplateSchema(TemplateBase):
    id: int

    class Config:
        from_attributes = True