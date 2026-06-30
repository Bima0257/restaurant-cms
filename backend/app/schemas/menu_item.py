from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    category_id: int
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool = True


class MenuItemUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None


class MenuItemOut(BaseModel):
    id: int
    category_id: int
    name: str
    slug: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    is_available: bool
    category_name: Optional[str] = None
    category_slug: str = ""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
