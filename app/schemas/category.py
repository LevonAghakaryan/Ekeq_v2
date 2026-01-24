from typing import Optional
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    image_url: Optional[str] = None

class CategorySchema(CategoryBase):
    id: int
    class Config:
        from_attributes = True