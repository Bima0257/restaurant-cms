from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CartItemCreate(BaseModel):
    menu_item_id: int
    qty: int = 1
    notes: Optional[str] = None


class CartItemUpdate(BaseModel):
    qty: int


class CartItemOut(BaseModel):
    id: int
    menu_item_id: int
    menu_item_name: Optional[str] = None
    menu_item_price: Optional[float] = None
    menu_item_image: Optional[str] = None
    qty: int
    notes: Optional[str] = None
    subtotal: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    payment_method: Optional[str] = None
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    menu_item_name: Optional[str] = None
    qty: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    order_number: str
    status: str
    total_price: float
    payment_method: Optional[str] = None
    payment_status: str
    delivery_address: Optional[str] = None
    notes: Optional[str] = None
    items: list[OrderItemOut] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str
