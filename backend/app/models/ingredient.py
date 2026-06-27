from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    unit: Mapped[str] = mapped_column(
        Enum("kg", "g", "pcs", "liter", "ml"),
        nullable=False,
    )
    stock_qty: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    min_stock: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    cost_per_unit: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    supplier_id: Mapped[Optional[int]] = mapped_column(ForeignKey("suppliers.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    recipes = relationship("Recipe", back_populates="ingredient")
    stock_transactions = relationship("StockTransaction", back_populates="ingredient")
    stock_alerts = relationship("StockAlert", back_populates="ingredient")
    supplier = relationship("Supplier", back_populates="ingredients")
