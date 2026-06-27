from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.response import (
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.routers import auth, customer, public_menu, staff
from app.routers.admin import categories, inventory, menu, orders, recipes
from app.routers import superadmin as superadmin_router
from app.routers import upload
from app.routers import reports
from app.routers import review

Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.BACKUP_DIR).mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="WorldPlate CMS API",
    description="Restaurant CMS with inventory management",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(public_menu.router)
app.include_router(customer.router)
app.include_router(staff.router)
app.include_router(menu.router)
app.include_router(categories.router)
app.include_router(inventory.router)
app.include_router(recipes.router)
app.include_router(orders.router)
app.include_router(superadmin_router.router)
app.include_router(upload.router)
app.include_router(reports.router)
app.include_router(review.router)


@app.get("/api/health")
def health_check():
    return {"success": True, "message": "WorldPlate CMS API is running"}
