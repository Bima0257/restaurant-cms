from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_staff
from app.models.ingredient import Ingredient
from app.models.order import Order
from app.models.stock_alert import StockAlert
from app.models.stock_transaction import StockTransaction
from app.models.user import User
from app.schemas.ingredient import IngredientOut
from app.schemas.order import OrderOut, OrderStatusUpdate
from app.schemas.stock import StockAdjustment, StockAlertOut, StockInCreate, StockTransactionOut
from app.services.stock_service import check_and_create_alerts, record_transaction

router = APIRouter(prefix="/api/staff", tags=["Staff"])


@router.get("/orders", response_model=list[OrderOut])
def list_orders(
    status: str | None = None,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    query = db.query(Order).order_by(Order.created_at.desc())
    if status:
        query = query.filter(Order.status == status)
    orders = query.all()

    result = []
    for order in orders:
        data = OrderOut.model_validate(order)
        data.items = []
        for item in order.items:
            from app.schemas.order import OrderItemOut

            item_data = OrderItemOut.model_validate(item)
            if item.menu_item:
                item_data.menu_item_name = item.menu_item.name
            data.items.append(item_data)
        result.append(data)
    return result


@router.put("/orders/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    allowed_statuses = ["confirmed", "preparing", "ready", "delivered", "completed"]
    if data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Allowed: {', '.join(allowed_statuses)}",
        )
    if data.status == "completed" and order.payment_status == "unpaid":
        order.payment_status = "paid"

    order.status = data.status
    db.commit()
    db.refresh(order)

    result = OrderOut.model_validate(order)
    result.items = []
    for item in order.items:
        from app.schemas.order import OrderItemOut

        item_data = OrderItemOut.model_validate(item)
        if item.menu_item:
            item_data.menu_item_name = item.menu_item.name
        result.items.append(item_data)
    return result


@router.get("/stock-check", response_model=list[IngredientOut])
def check_stock(
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.is_active == True)
        .order_by(Ingredient.name)
        .all()
    )
    result = []
    for ing in ingredients:
        data = IngredientOut.model_validate(ing)
        if ing.supplier:
            data.supplier_name = ing.supplier.name
        result.append(data)
    return result


@router.get("/alerts", response_model=list[StockAlertOut])
def list_alerts(
    unresolved_only: bool = True,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    query = db.query(StockAlert).order_by(StockAlert.created_at.desc())
    if unresolved_only:
        query = query.filter(StockAlert.is_resolved == False)
    alerts = query.all()

    result = []
    for alert in alerts:
        data = StockAlertOut.model_validate(alert)
        if alert.ingredient:
            data.ingredient_name = alert.ingredient.name
            data.ingredient_sku = alert.ingredient.sku
            data.stock_qty = float(alert.ingredient.stock_qty)
            data.min_stock = float(alert.ingredient.min_stock)
        result.append(data)
    return result


@router.post("/stock-in", response_model=StockTransactionOut)
def staff_stock_in(
    data: StockInCreate,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    try:
        tx = record_transaction(
            db=db,
            ingredient_id=data.ingredient_id,
            type="IN",
            qty=data.qty,
            reference_type="purchase",
            notes=data.notes,
            created_by=current_user.id,
        )
        db.commit()
        db.refresh(tx)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = StockTransactionOut.model_validate(tx)
    if tx.ingredient:
        result.ingredient_name = tx.ingredient.name
    return result


@router.post("/stock/adjust", response_model=StockTransactionOut)
def staff_adjust_stock(
    data: StockAdjustment,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    try:
        tx = record_transaction(
            db=db,
            ingredient_id=data.ingredient_id,
            type="ADJUSTMENT",
            qty=data.qty,
            reference_type="manual",
            notes=data.notes,
            created_by=current_user.id,
        )
        db.commit()
        db.refresh(tx)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = StockTransactionOut.model_validate(tx)
    if tx.ingredient:
        result.ingredient_name = tx.ingredient.name
    return result


@router.put("/alerts/{alert_id}/resolve", response_model=StockAlertOut)
def staff_resolve_alert(
    alert_id: int,
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db),
):
    alert = db.query(StockAlert).filter(StockAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_resolved = True
    alert.resolved_by = current_user.id
    alert.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)

    data = StockAlertOut.model_validate(alert)
    if alert.ingredient:
        data.ingredient_name = alert.ingredient.name
        data.ingredient_sku = alert.ingredient.sku
        data.stock_qty = float(alert.ingredient.stock_qty)
        data.min_stock = float(alert.ingredient.min_stock)
    return data
