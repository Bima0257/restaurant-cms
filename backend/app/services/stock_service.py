from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.models.stock_alert import StockAlert
from app.models.stock_transaction import StockTransaction


def check_and_create_alerts(db: Session, ingredient_id: int) -> list[StockAlert]:
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        return []

    alerts = []
    existing = (
        db.query(StockAlert)
        .filter(
            StockAlert.ingredient_id == ingredient_id,
            StockAlert.is_resolved == False,
        )
        .first()
    )
    if existing:
        return []

    if ingredient.stock_qty <= 0:
        alert = StockAlert(
            ingredient_id=ingredient_id,
            type="out_of_stock",
            message=f"{ingredient.name} is out of stock (SKU: {ingredient.sku})",
        )
        db.add(alert)
        alerts.append(alert)

        ingredient.is_active = False
    elif ingredient.stock_qty <= ingredient.min_stock:
        alert = StockAlert(
            ingredient_id=ingredient_id,
            type="low_stock",
            message=f"{ingredient.name} is running low: {ingredient.stock_qty} {ingredient.unit} remaining (min: {ingredient.min_stock})",
        )
        db.add(alert)
        alerts.append(alert)

    db.flush()
    return alerts


def record_transaction(
    db: Session,
    ingredient_id: int,
    type: str,
    qty: float,
    reference_type: str | None = None,
    reference_id: int | None = None,
    notes: str | None = None,
    created_by: int | None = None,
) -> StockTransaction:
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise ValueError(f"Ingredient {ingredient_id} not found")

    tx = StockTransaction(
        ingredient_id=ingredient_id,
        type=type,
        qty=qty,
        reference_type=reference_type,
        reference_id=reference_id,
        notes=notes,
        created_by=created_by,
    )
    db.add(tx)

    if type == "IN":
        ingredient.stock_qty += qty
        ingredient.is_active = True
    elif type == "OUT":
        ingredient.stock_qty -= qty
    elif type == "ADJUSTMENT":
        ingredient.stock_qty += qty

    db.flush()
    check_and_create_alerts(db, ingredient_id)
    return tx


def bulk_deduct_stock(
    db: Session,
    deductions: list[dict],
    reference_id: int | None = None,
    created_by: int | None = None,
) -> list[StockTransaction]:
    transactions = []
    for d in deductions:
        tx = record_transaction(
            db=db,
            ingredient_id=d["ingredient_id"],
            type="OUT",
            qty=d["qty"],
            reference_type="order",
            reference_id=reference_id,
            notes=d.get("notes"),
            created_by=created_by,
        )
        transactions.append(tx)
    return transactions


def check_menu_stock(
    db: Session,
    recipe_requirements: list[dict],
) -> tuple[bool, list[dict]]:
    details = []
    all_available = True
    for req in recipe_requirements:
        ingredient = (
            db.query(Ingredient)
            .filter(Ingredient.id == req["ingredient_id"])
            .first()
        )
        if not ingredient:
            details.append(
                {
                    "ingredient_id": req["ingredient_id"],
                    "available": False,
                    "reason": "Ingredient not found",
                }
            )
            all_available = False
            continue

        needed = req["qty_needed"] * req["qty"]
        if ingredient.stock_qty < needed:
            details.append(
                {
                    "ingredient_id": ingredient.id,
                    "name": ingredient.name,
                    "available": False,
                    "stock": float(ingredient.stock_qty),
                    "needed": float(needed),
                    "unit": ingredient.unit,
                }
            )
            all_available = False
        else:
            details.append(
                {
                    "ingredient_id": ingredient.id,
                    "name": ingredient.name,
                    "available": True,
                    "stock": float(ingredient.stock_qty),
                    "needed": float(needed),
                    "unit": ingredient.unit,
                }
            )
    return all_available, details
