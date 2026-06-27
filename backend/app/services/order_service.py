from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.models.recipe import Recipe
from app.services.stock_service import bulk_deduct_stock, check_menu_stock


def generate_order_number(db: Session) -> str:
    last_order = (
        db.query(Order).order_by(Order.id.desc()).first()
    )
    next_id = (last_order.id + 1) if last_order else 1
    return f"WP-{next_id:04d}"


def process_checkout(
    db: Session,
    user_id: int,
    payment_method: str | None = None,
    delivery_address: str | None = None,
    notes: str | None = None,
) -> Order:
    cart_items = (
        db.query(Cart)
        .filter(Cart.user_id == user_id)
        .all()
    )
    if not cart_items:
        raise ValueError("Cart is empty")

    recipe_requirements = []
    order_items_data = []
    total = 0.0

    for cart_item in cart_items:
        menu_item = (
            db.query(MenuItem)
            .filter(MenuItem.id == cart_item.menu_item_id)
            .first()
        )
        if not menu_item or not menu_item.is_available:
            raise ValueError(f"Menu item {cart_item.menu_item_id} is not available")

        recipes = (
            db.query(Recipe)
            .filter(Recipe.menu_item_id == menu_item.id)
            .all()
        )

        for recipe in recipes:
            recipe_requirements.append(
                {
                    "ingredient_id": recipe.ingredient_id,
                    "qty_needed": float(recipe.qty_needed),
                    "qty": cart_item.qty,
                }
            )

        subtotal = float(menu_item.price) * cart_item.qty
        total += subtotal
        order_items_data.append(
            {
                "menu_item_id": menu_item.id,
                "qty": cart_item.qty,
                "unit_price": float(menu_item.price),
                "subtotal": subtotal,
            }
        )

    if recipe_requirements:
        all_available, details = check_menu_stock(db, recipe_requirements)
        if not all_available:
            unavailable = [
                d for d in details if not d["available"]
            ]
            raise ValueError(
                f"Insufficient stock for ingredients: {unavailable}"
            )

    order_number = generate_order_number(db)
    order = Order(
        user_id=user_id,
        order_number=order_number,
        status="pending",
        total_price=total,
        payment_method=payment_method,
        payment_status="unpaid",
        delivery_address=delivery_address,
        notes=notes,
    )
    db.add(order)
    db.flush()

    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            **item_data,
        )
        db.add(order_item)

    if recipe_requirements:
        bulk_deduct_stock(
            db=db,
            deductions=[
                {
                    "ingredient_id": req["ingredient_id"],
                    "qty": float(req["qty_needed"]) * req["qty"],
                    "notes": f"Order #{order_number}",
                }
                for req in recipe_requirements
            ],
            reference_id=order.id,
        )

    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.flush()

    return order
