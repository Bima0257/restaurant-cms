from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ingredient_id: Mapped[int] = mapped_column(ForeignKey("ingredients.id"), nullable=False)
    type: Mapped[str] = mapped_column(
        Enum("IN", "OUT", "ADJUSTMENT"),
        nullable=False,
    )
    qty: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    reference_type: Mapped[Optional[str]] = mapped_column(
        Enum("purchase", "order", "manual"),
        nullable=True,
    )
    reference_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    ingredient = relationship("Ingredient", back_populates="stock_transactions")
    created_by_user = relationship("User", back_populates="stock_transactions")
