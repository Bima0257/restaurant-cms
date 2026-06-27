from app.database import SessionLocal, engine, Base
from app.dependencies import hash_password
from app.models.user import User
from app.models.category import Category
from app.models.ingredient import Ingredient
from app.models.supplier import Supplier
from app.models.menu_item import MenuItem
from app.models.recipe import Recipe


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(User).first():
        print("Database already seeded. Skipping.")
        db.close()
        return

    # Superadmin
    superadmin = User(
        email="superadmin@worldplate.com",
        hashed_password=hash_password("admin123"),
        full_name="Super Admin",
        role="superadmin",
        is_active=True,
    )
    db.add(superadmin)

    # Admin
    admin = User(
        email="admin@worldplate.com",
        hashed_password=hash_password("admin123"),
        full_name="Restaurant Admin",
        role="admin",
        is_active=True,
    )
    db.add(admin)

    # Staff
    staff = User(
        email="staff@worldplate.com",
        hashed_password=hash_password("staff123"),
        full_name="Staff Member",
        role="staff",
        is_active=True,
    )
    db.add(staff)

    # Customer
    customer = User(
        email="customer@example.com",
        hashed_password=hash_password("cust123"),
        full_name="John Customer",
        role="customer",
        is_active=True,
        is_verified=True,
    )
    db.add(customer)

    # Suppliers
    supplier1 = Supplier(name="Fresh Foods Supply", contact_person="Bob", phone="08123456789")
    supplier2 = Supplier(name="Global Ingredients Ltd", contact_person="Alice", phone="08198765432")
    db.add_all([supplier1, supplier2])

    # Categories
    pizza = Category(name="Pizza", slug="pizza", sort_order=1)
    burger = Category(name="Burgers", slug="burgers", sort_order=2)
    sushi = Category(name="Sushi", slug="sushi", sort_order=3)
    breakfast = Category(name="Breakfast", slug="breakfast", sort_order=4)
    noodles = Category(name="Noodles", slug="noodles", sort_order=5)
    db.add_all([pizza, burger, sushi, breakfast, noodles])

    # Ingredients
    flour = Ingredient(name="Flour", sku="FLO-001", unit="kg", stock_qty=50, min_stock=10, cost_per_unit=2.5, supplier_id=1)
    cheese = Ingredient(name="Mozzarella Cheese", sku="CHS-001", unit="kg", stock_qty=20, min_stock=5, cost_per_unit=8.0, supplier_id=1)
    tomato_sauce = Ingredient(name="Tomato Sauce", sku="SAU-001", unit="liter", stock_qty=30, min_stock=10, cost_per_unit=3.0, supplier_id=2)
    beef_patty = Ingredient(name="Beef Patty", sku="BEEF-001", unit="pcs", stock_qty=100, min_stock=20, cost_per_unit=4.5, supplier_id=1)
    burger_bun = Ingredient(name="Burger Bun", sku="BUN-001", unit="pcs", stock_qty=80, min_stock=20, cost_per_unit=1.0, supplier_id=2)
    salmon = Ingredient(name="Atlantic Salmon", sku="FSH-001", unit="kg", stock_qty=15, min_stock=5, cost_per_unit=15.0, supplier_id=2)
    rice = Ingredient(name="Sushi Rice", sku="RIC-001", unit="kg", stock_qty=30, min_stock=10, cost_per_unit=3.5, supplier_id=1)
    eggs = Ingredient(name="Eggs", sku="EGG-001", unit="pcs", stock_qty=200, min_stock=50, cost_per_unit=0.3, supplier_id=1)
    ramen_noodles = Ingredient(name="Ramen Noodles", sku="NOD-001", unit="kg", stock_qty=25, min_stock=8, cost_per_unit=4.0, supplier_id=2)
    db.add_all([flour, cheese, tomato_sauce, beef_patty, burger_bun, salmon, rice, eggs, ramen_noodles])
    db.flush()

    # Menu Items
    margherita = MenuItem(name="Margherita Pizza", slug="margherita-pizza", category_id=pizza.id, price=19.00, description="Classic tomato, mozzarella, and basil")
    signature_burger = MenuItem(name="Signature Burger", slug="signature-burger", category_id=burger.id, price=24.00, description="Double patties, melted gouda, secret sauce")
    salmon_sushi = MenuItem(name="Salmon Sushi Set", slug="salmon-sushi-set", category_id=sushi.id, price=32.00, description="Fresh Atlantic salmon with premium wasabi")
    breakfast_specials = MenuItem(name="Breakfast Specials", slug="breakfast-specials", category_id=breakfast.id, price=99.00, description="Fluffy eggs, crispy bacon, artisan toast")
    ramen_bowl = MenuItem(name="Ramen Bowl", slug="ramen-bowl", category_id=noodles.id, price=28.00, description="Golden broth with noodles and soft-boiled egg")
    db.add_all([margherita, signature_burger, salmon_sushi, breakfast_specials, ramen_bowl])
    db.flush()

    # Recipes (BOM)
    recipes_data = [
        (margherita.id, flour.id, 0.3, "kg"),
        (margherita.id, cheese.id, 0.2, "kg"),
        (margherita.id, tomato_sauce.id, 0.15, "liter"),
        (signature_burger.id, beef_patty.id, 2, "pcs"),
        (signature_burger.id, burger_bun.id, 1, "pcs"),
        (signature_burger.id, cheese.id, 0.05, "kg"),
        (salmon_sushi.id, salmon.id, 0.2, "kg"),
        (salmon_sushi.id, rice.id, 0.15, "kg"),
        (breakfast_specials.id, eggs.id, 3, "pcs"),
        (ramen_bowl.id, ramen_noodles.id, 0.2, "kg"),
        (ramen_bowl.id, eggs.id, 1, "pcs"),
    ]
    for menu_id, ing_id, qty, unit in recipes_data:
        db.add(Recipe(menu_item_id=menu_id, ingredient_id=ing_id, qty_needed=qty, unit=unit))

    db.commit()
    db.close()
    print("Database seeded successfully!")
    print("")
    print("Login Credentials:")
    print("  Superadmin: superadmin@worldplate.com / admin123")
    print("  Admin:      admin@worldplate.com / admin123")
    print("  Staff:      staff@worldplate.com / staff123")
    print("  Customer:   customer@example.com / cust123")


if __name__ == "__main__":
    seed()
