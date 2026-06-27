from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewOut

router = APIRouter(prefix="/api", tags=["Reviews"])


@router.post("/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can submit reviews",
        )

    menu_item = db.query(MenuItem).filter(MenuItem.id == data.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    existing = (
        db.query(Review)
        .filter(
            Review.menu_item_id == data.menu_item_id,
            Review.user_id == current_user.id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this menu item",
        )

    has_ordered = (
        db.query(Order)
        .join(OrderItem)
        .filter(
            Order.user_id == current_user.id,
            OrderItem.menu_item_id == data.menu_item_id,
            Order.status.in_(["completed", "delivered"]),
        )
        .first()
    )
    if not has_ordered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only review items you have ordered",
        )

    review = Review(
        menu_item_id=data.menu_item_id,
        user_id=current_user.id,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    result = ReviewOut.model_validate(review)
    result.full_name = current_user.full_name
    result.menu_item_name = menu_item.name
    return result


@router.get("/menu/{menu_item_id}/reviews", response_model=list[ReviewOut])
def list_menu_reviews(
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    reviews = (
        db.query(Review)
        .filter(Review.menu_item_id == menu_item_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    result = []
    for r in reviews:
        data = ReviewOut.model_validate(r)
        data.full_name = r.user.full_name if r.user else "-"
        data.menu_item_name = menu_item.name
        result.append(data)
    return result


@router.get("/menu/{menu_item_id}/rating")
def get_menu_rating(
    menu_item_id: int,
    db: Session = Depends(get_db),
):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    stats = (
        db.query(
            func.count(Review.id).label("count"),
            func.coalesce(func.avg(Review.rating), 0).label("average"),
        )
        .filter(Review.menu_item_id == menu_item_id)
        .first()
    )
    return {
        "menu_item_id": menu_item_id,
        "menu_item_name": menu_item.name,
        "average_rating": round(float(stats.average), 1),
        "total_reviews": stats.count,
    }


@router.get("/my-reviews", response_model=list[ReviewOut])
def list_my_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reviews = (
        db.query(Review)
        .filter(Review.user_id == current_user.id)
        .order_by(Review.created_at.desc())
        .all()
    )
    result = []
    for r in reviews:
        data = ReviewOut.model_validate(r)
        data.full_name = current_user.full_name
        data.menu_item_name = r.menu_item.name if r.menu_item else "-"
        result.append(data)
    return result


@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    review = (
        db.query(Review)
        .filter(Review.id == review_id, Review.user_id == current_user.id)
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}
