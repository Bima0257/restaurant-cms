from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.models.user import User
from app.schemas.menu_item import MenuItemCreate, MenuItemOut, MenuItemUpdate
from app.services.audit_service import get_client_info, log_activity

router = APIRouter(prefix="/api/admin/menu", tags=["Admin - Menu"])


@router.get("", response_model=list[MenuItemOut])
def list_menu(
    category_id: int | None = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(MenuItem).order_by(MenuItem.name)
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    items = query.all()
    result = []
    for item in items:
        data = MenuItemOut.model_validate(item)
        if item.category:
            data.category_name = item.category.name
        result.append(data)
    return result


@router.get("/{item_id}", response_model=MenuItemOut)
def get_menu_item(
    item_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    data = MenuItemOut.model_validate(item)
    if item.category:
        data.category_name = item.category.name
    return data


@router.post("", response_model=MenuItemOut, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    data: MenuItemCreate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if not db.query(Category).filter(Category.id == data.category_id).first():
        raise HTTPException(status_code=404, detail="Category not found")
    if db.query(MenuItem).filter(MenuItem.slug == data.slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")

    item = MenuItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Create Menu Item", module="Menu", description=f"Created: {item.name}", ip_address=ip, user_agent=ua)

    result = MenuItemOut.model_validate(item)
    if item.category:
        result.category_name = item.category.name
    return result


@router.put("/{item_id}", response_model=MenuItemOut)
def update_menu_item(
    item_id: int,
    data: MenuItemUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Menu Item", module="Menu", description=f"Updated: {item.name}", ip_address=ip, user_agent=ua)

    result = MenuItemOut.model_validate(item)
    if item.category:
        result.category_name = item.category.name
    return result


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Menu Item", module="Menu", description=f"Deleted: {item.name}", ip_address=ip, user_agent=ua)

    db.delete(item)
    db.commit()
