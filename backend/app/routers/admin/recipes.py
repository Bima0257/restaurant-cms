from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_admin
from app.models.ingredient import Ingredient
from app.models.menu_item import MenuItem
from app.models.recipe import Recipe
from app.models.user import User
from app.schemas.recipe import RecipeCreate, RecipeOut, StockCheckResult
from app.services.audit_service import get_client_info, log_activity
from app.services.stock_service import check_menu_stock

router = APIRouter(prefix="/api/admin/recipes", tags=["Admin - Recipes"])


@router.get("/by-menu/{menu_item_id}", response_model=list[RecipeOut])
def list_recipes_by_menu(
    menu_item_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    recipes = (
        db.query(Recipe)
        .filter(Recipe.menu_item_id == menu_item_id)
        .all()
    )
    result = []
    for recipe in recipes:
        data = RecipeOut.model_validate(recipe)
        if recipe.ingredient:
            data.ingredient_name = recipe.ingredient.name
            data.ingredient_unit = recipe.ingredient.unit
        result.append(data)
    return result


@router.post("", response_model=RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe(
    data: RecipeCreate,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if not db.query(MenuItem).filter(MenuItem.id == data.menu_item_id).first():
        raise HTTPException(status_code=404, detail="Menu item not found")
    if not db.query(Ingredient).filter(Ingredient.id == data.ingredient_id).first():
        raise HTTPException(status_code=404, detail="Ingredient not found")

    existing = (
        db.query(Recipe)
        .filter(
            Recipe.menu_item_id == data.menu_item_id,
            Recipe.ingredient_id == data.ingredient_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="Recipe entry for this ingredient already exists"
        )

    recipe = Recipe(**data.model_dump())
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    ip, ua = get_client_info(request)
    ing_name = recipe.ingredient.name if recipe.ingredient else "-"
    log_activity(db, current_user, "Create Recipe", module="Recipe", description=f"Added {ing_name} to menu item {data.menu_item_id}", ip_address=ip, user_agent=ua)

    result = RecipeOut.model_validate(recipe)
    if recipe.ingredient:
        result.ingredient_name = recipe.ingredient.name
        result.ingredient_unit = recipe.ingredient.unit
    return result


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ip, ua = get_client_info(request)
    log_activity(db, current_user, "Delete Recipe", module="Recipe", description=f"Deleted recipe id {recipe_id}", ip_address=ip, user_agent=ua)

    db.delete(recipe)
    db.commit()


@router.get("/check-stock/{menu_item_id}/{qty}", response_model=StockCheckResult)
def check_stock_for_menu(
    menu_item_id: int,
    qty: int = 1,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    recipes = (
        db.query(Recipe)
        .filter(Recipe.menu_item_id == menu_item_id)
        .all()
    )
    if not recipes:
        return StockCheckResult(
            menu_item_id=menu_item_id,
            menu_item_name=menu_item.name,
            is_available=True,
            details=[],
        )

    requirements = [
        {
            "ingredient_id": r.ingredient_id,
            "qty_needed": float(r.qty_needed),
            "qty": qty,
        }
        for r in recipes
    ]

    is_available, details = check_menu_stock(db, requirements)
    return StockCheckResult(
        menu_item_id=menu_item_id,
        menu_item_name=menu_item.name,
        is_available=is_available,
        details=details,
    )
