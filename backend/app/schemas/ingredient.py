from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class IngredientCreate(BaseModel):
    name: str
    sku: str
    category: Optional[str] = None
    unit: str
    stock_qty: float = 0
    min_stock: float = 0
    cost_per_unit: Optional[float] = None
    supplier_id: Optional[int] = None


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    stock_qty: Optional[float] = None
    min_stock: Optional[float] = None
    cost_per_unit: Optional[float] = None
    supplier_id: Optional[int] = None
    is_active: Optional[bool] = None


class IngredientOut(BaseModel):
    id: int
    name: str
    sku: str
    category: Optional[str] = None
    unit: str
    stock_qty: float
    min_stock: float
    cost_per_unit: Optional[float] = None
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
