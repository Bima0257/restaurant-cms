from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ReviewCreate(BaseModel):
    menu_item_id: int
    rating: int
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: int) -> int:
        if v < 1 or v > 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewOut(BaseModel):
    id: int
    menu_item_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    full_name: str = ""
    menu_item_name: str = ""

    class Config:
        from_attributes = True
