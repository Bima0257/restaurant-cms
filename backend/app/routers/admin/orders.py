from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.order import Order
from app.models.user import User
from app.schemas.order import OrderOut, OrderStatusUpdate
from app.services.audit_service import get_client_info, log_activity

router = APIRouter(prefix="/api/admin/orders", tags=["Admin - Orders"])


@router.get("", response_model=list[OrderOut])
def list_orders(
    status: str | None = None,
    current_user: User = Depends(require_admin),
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


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    data = OrderOut.model_validate(order)
    data.items = []
    for item in order.items:
        from app.schemas.order import OrderItemOut

        item_data = OrderItemOut.model_validate(item)
        if item.menu_item:
            item_data.menu_item_name = item.menu_item.name
        data.items.append(item_data)
    return data


@router.put("/{order_id}/status", response_model=OrderOut)
def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    old_status = order.status
    if data.status == "cancelled":
        order.payment_status = "refunded"
    if data.status == "completed" and order.payment_status == "unpaid":
        order.payment_status = "paid"

    order.status = data.status
    db.commit()
    db.refresh(order)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Order Status", module="Orders", description=f"Order #{order.order_number}: {old_status} -> {data.status}", ip_address=ip, user_agent=ua)

    result = OrderOut.model_validate(order)
    result.items = []
    for item in order.items:
        from app.schemas.order import OrderItemOut

        item_data = OrderItemOut.model_validate(item)
        if item.menu_item:
            item_data.menu_item_name = item.menu_item.name
        result.items.append(item_data)
    return result
