from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate
from app.services.audit_service import get_client_info, log_activity

router = APIRouter(prefix="/api/admin/categories", tags=["Admin - Categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(Category).order_by(Category.sort_order).all()


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(
    category_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if db.query(Category).filter(Category.slug == data.slug).first():
        raise HTTPException(status_code=400, detail="Slug already exists")
    cat = Category(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Create Category", module="Category", description=f"Created: {cat.name}", ip_address=ip, user_agent=ua)

    return cat


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Update Category", module="Category", description=f"Updated: {cat.name}", ip_address=ip, user_agent=ua)

    return cat


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Category", module="Category", description=f"Deleted: {cat.name}", ip_address=ip, user_agent=ua)

    db.delete(cat)
    db.commit()
