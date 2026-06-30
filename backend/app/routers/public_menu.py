from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.schemas.category import CategoryOut
from app.schemas.menu_item import MenuItemOut

router = APIRouter(prefix="/api", tags=["Public"])


@router.get("/menu", response_model=list[MenuItemOut])
def list_menu(
    category_slug: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(MenuItem).filter(MenuItem.is_available == True)
    if category_slug:
        category = (
            db.query(Category)
            .filter(Category.slug == category_slug)
            .first()
        )
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        query = query.filter(MenuItem.category_id == category.id)

    items = query.all()
    result = []
    for item in items:
        data = MenuItemOut.model_validate(item)
        if item.category:
            data.category_name = item.category.name
            data.category_slug = item.category.slug
        result.append(data)
    return result


@router.get("/menu/{item_id}", response_model=MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    data = MenuItemOut.model_validate(item)
    if item.category:
        data.category_name = item.category.name
        data.category_slug = item.category.slug
    return data


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.is_active == True).all()
