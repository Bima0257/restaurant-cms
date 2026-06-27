from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.ingredient import Ingredient
from app.models.stock_alert import StockAlert
from app.models.stock_transaction import StockTransaction
from app.models.supplier import Supplier
from app.models.user import User
from app.schemas.ingredient import IngredientCreate, IngredientOut, IngredientUpdate
from app.schemas.stock import (
    StockAdjustment,
    StockAlertOut,
    StockInCreate,
    StockTransactionOut,
)
from app.schemas.supplier import SupplierCreate, SupplierOut, SupplierUpdate
from app.services.audit_service import get_client_info, log_activity
from app.services.stock_service import record_transaction

router = APIRouter(prefix="/api/admin/inventory", tags=["Admin - Inventory"])


@router.get("/ingredients", response_model=list[IngredientOut])
def list_ingredients(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    ingredients = db.query(Ingredient).order_by(Ingredient.name).all()
    result = []
    for ing in ingredients:
        data = IngredientOut.model_validate(ing)
        if ing.supplier:
            data.supplier_name = ing.supplier.name
        result.append(data)
    return result


@router.get("/ingredients/{ingredient_id}", response_model=IngredientOut)
def get_ingredient(
    ingredient_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    ing = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    data = IngredientOut.model_validate(ing)
    if ing.supplier:
        data.supplier_name = ing.supplier.name
    return data


@router.post(
    "/ingredients",
    response_model=IngredientOut,
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(
    data: IngredientCreate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if db.query(Ingredient).filter(Ingredient.sku == data.sku).first():
        raise HTTPException(status_code=400, detail="SKU already exists")
    ing = Ingredient(**data.model_dump())
    db.add(ing)
    db.commit()
    db.refresh(ing)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Create Ingredient", module="Inventory", description=f"Created: {ing.name}", ip_address=ip, user_agent=ua)

    result = IngredientOut.model_validate(ing)
    if ing.supplier:
        result.supplier_name = ing.supplier.name
    return result


@router.put("/ingredients/{ingredient_id}", response_model=IngredientOut)
def update_ingredient(
    ingredient_id: int,
    data: IngredientUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    ing = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ing, field, value)
    db.commit()
    db.refresh(ing)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Ingredient", module="Inventory", description=f"Updated: {ing.name}", ip_address=ip, user_agent=ua)

    result = IngredientOut.model_validate(ing)
    if ing.supplier:
        result.supplier_name = ing.supplier.name
    return result


@router.delete("/ingredients/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    ing = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Ingredient", module="Inventory", description=f"Deleted: {ing.name}", ip_address=ip, user_agent=ua)

    db.delete(ing)
    db.commit()


@router.post("/stock-in", response_model=StockTransactionOut)
def stock_in(
    data: StockInCreate,
    request: Request,
    current_user: User = Depends(require_admin),
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

    ip, ua = get_client_info(request)
    ing_name = tx.ingredient.name if tx.ingredient else "-"
    log_activity(db, current_user, "Stock In", module="Inventory", description=f"{ing_name}: +{data.qty}", ip_address=ip, user_agent=ua)

    result = StockTransactionOut.model_validate(tx)
    if tx.ingredient:
        result.ingredient_name = tx.ingredient.name
    return result


@router.post("/adjust", response_model=StockTransactionOut)
def adjust_stock(
    data: StockAdjustment,
    request: Request,
    current_user: User = Depends(require_admin),
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

    ip, ua = get_client_info(request)
    ing_name = tx.ingredient.name if tx.ingredient else "-"
    log_activity(db, current_user, "Stock Adjustment", module="Inventory", description=f"{ing_name}: adj {data.qty}", ip_address=ip, user_agent=ua)

    result = StockTransactionOut.model_validate(tx)
    if tx.ingredient:
        result.ingredient_name = tx.ingredient.name
    return result


@router.get("/transactions", response_model=list[StockTransactionOut])
def list_transactions(
    ingredient_id: int | None = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(StockTransaction).order_by(StockTransaction.created_at.desc())
    if ingredient_id:
        query = query.filter(StockTransaction.ingredient_id == ingredient_id)
    txs = query.all()
    result = []
    for tx in txs:
        data = StockTransactionOut.model_validate(tx)
        if tx.ingredient:
            data.ingredient_name = tx.ingredient.name
        if tx.created_by_user:
            data.created_by_name = tx.created_by_user.full_name
        result.append(data)
    return result


@router.get("/alerts", response_model=list[StockAlertOut])
def list_alerts(
    unresolved_only: bool = True,
    current_user: User = Depends(require_admin),
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


@router.put("/alerts/{alert_id}/resolve", response_model=StockAlertOut)
def resolve_alert(
    alert_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
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

    ip, ua = get_client_info(request)
    ing_name = alert.ingredient.name if alert.ingredient else "-"
    log_activity(db, current_user, "Resolve Stock Alert", module="Inventory", description=f"Resolved alert for: {ing_name}", ip_address=ip, user_agent=ua)

    data = StockAlertOut.model_validate(alert)
    if alert.ingredient:
        data.ingredient_name = alert.ingredient.name
        data.ingredient_sku = alert.ingredient.sku
        data.stock_qty = float(alert.ingredient.stock_qty)
        data.min_stock = float(alert.ingredient.min_stock)
    return data


@router.get("/suppliers", response_model=list[SupplierOut])
def list_suppliers(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(Supplier).order_by(Supplier.name).all()


@router.get("/suppliers/{supplier_id}", response_model=SupplierOut)
def get_supplier(
    supplier_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.post(
    "/suppliers", response_model=SupplierOut, status_code=status.HTTP_201_CREATED
)
def create_supplier(
    data: SupplierCreate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    supplier = Supplier(**data.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Create Supplier", module="Inventory", description=f"Created: {supplier.name}", ip_address=ip, user_agent=ua)

    return supplier


@router.put("/suppliers/{supplier_id}", response_model=SupplierOut)
def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Supplier", module="Inventory", description=f"Updated: {supplier.name}", ip_address=ip, user_agent=ua)

    return supplier


@router.delete(
    "/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_supplier(
    supplier_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Supplier", module="Inventory", description=f"Deleted: {supplier.name}", ip_address=ip, user_agent=ua)

    db.delete(supplier)
    db.commit()
