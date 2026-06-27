from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StockInCreate(BaseModel):
    ingredient_id: int
    qty: float
    notes: Optional[str] = None


class StockAdjustment(BaseModel):
    ingredient_id: int
    qty: float
    notes: Optional[str] = None


class StockTransactionOut(BaseModel):
    id: int
    ingredient_id: int
    ingredient_name: Optional[str] = None
    type: str
    qty: float
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    notes: Optional[str] = None
    created_by: Optional[int] = None
    created_by_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class StockAlertOut(BaseModel):
    id: int
    ingredient_id: int
    ingredient_name: Optional[str] = None
    ingredient_sku: Optional[str] = None
    stock_qty: Optional[float] = None
    min_stock: Optional[float] = None
    type: str
    message: Optional[str] = None
    is_resolved: bool
    resolved_by: Optional[int] = None
    resolved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
