from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.cart import Cart
from app.models.menu_item import MenuItem
from app.models.order import Order
from app.models.user import User
from app.schemas.order import (
    CartItemCreate,
    CartItemOut,
    CartItemUpdate,
    OrderCreate,
    OrderItemOut,
    OrderOut,
)
from app.services.order_service import process_checkout

router = APIRouter(prefix="/api", tags=["Customer"])


@router.get("/cart", response_model=list[CartItemOut])
def list_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id)
        .all()
    )
    result = []
    for item in items:
        data = CartItemOut.model_validate(item)
        if item.menu_item:
            data.menu_item_name = item.menu_item.name
            data.menu_item_price = float(item.menu_item.price)
            data.menu_item_image = item.menu_item.image_url
            data.subtotal = float(item.menu_item.price) * item.qty
        result.append(data)
    return result


@router.post("/cart", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    data: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    menu_item = db.query(MenuItem).filter(MenuItem.id == data.menu_item_id).first()
    if not menu_item or not menu_item.is_available:
        raise HTTPException(status_code=404, detail="Menu item not available")

    existing = (
        db.query(Cart)
        .filter(
            Cart.user_id == current_user.id,
            Cart.menu_item_id == data.menu_item_id,
        )
        .first()
    )
    if existing:
        existing.qty += data.qty
        db.commit()
        db.refresh(existing)
        cart_item = existing
    else:
        cart_item = Cart(
            user_id=current_user.id,
            menu_item_id=data.menu_item_id,
            qty=data.qty,
            notes=data.notes,
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)

    result = CartItemOut.model_validate(cart_item)
    result.menu_item_name = menu_item.name
    result.menu_item_price = float(menu_item.price)
    result.menu_item_image = menu_item.image_url
    result.subtotal = float(menu_item.price) * cart_item.qty
    return result


@router.put("/cart/{item_id}", response_model=CartItemOut)
def update_cart(
    item_id: int,
    data: CartItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(Cart)
        .filter(Cart.id == item_id, Cart.user_id == current_user.id)
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.qty = data.qty
    db.commit()
    db.refresh(cart_item)

    result = CartItemOut.model_validate(cart_item)
    if cart_item.menu_item:
        result.menu_item_name = cart_item.menu_item.name
        result.menu_item_price = float(cart_item.menu_item.price)
        result.menu_item_image = cart_item.menu_item.image_url
        result.subtotal = float(cart_item.menu_item.price) * cart_item.qty
    return result


@router.delete("/cart/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_item = (
        db.query(Cart)
        .filter(Cart.id == item_id, Cart.user_id == current_user.id)
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()


@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        order = process_checkout(
            db=db,
            user_id=current_user.id,
            payment_method=data.payment_method,
            delivery_address=data.delivery_address,
            notes=data.notes,
        )
        db.commit()
        db.refresh(order)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return _order_to_out(order)


@router.get("/orders", response_model=list[OrderOut])
def list_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_order_to_out(o) for o in orders]


@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _order_to_out(order)


@router.put("/orders/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(
            status_code=400, detail="Only pending orders can be cancelled"
        )
    order.status = "cancelled"
    db.commit()
    db.refresh(order)
    return _order_to_out(order)


def _order_to_out(order: Order) -> OrderOut:
    data = OrderOut.model_validate(order)
    data.items = []
    for item in order.items:
        item_data = OrderItemOut.model_validate(item)
        if item.menu_item:
            item_data.menu_item_name = item.menu_item.name
        data.items.append(item_data)
    return data
