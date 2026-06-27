from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecipeCreate(BaseModel):
    menu_item_id: int
    ingredient_id: int
    qty_needed: float
    unit: str


class RecipeOut(BaseModel):
    id: int
    menu_item_id: int
    ingredient_id: int
    qty_needed: float
    unit: str
    ingredient_name: Optional[str] = None
    ingredient_unit: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockCheckResult(BaseModel):
    menu_item_id: int
    menu_item_name: str
    is_available: bool
    details: list[dict]
