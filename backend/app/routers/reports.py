from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.services.report_service import (
    generate_activity_report,
    generate_best_menu_report,
    generate_orders_report,
    generate_sales_report,
    generate_stock_report,
    generate_usage_report,
)

router = APIRouter(prefix="/api/reports", tags=["Reports"])


def _pdf_response(pdf_bytes: bytes, filename: str) -> Response:
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}.pdf"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )


@router.get("/sales")
def sales_report(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    pdf = generate_sales_report(db, start_date, end_date)
    return _pdf_response(pdf, "sales_report")


@router.get("/orders")
def orders_report(
    start_date: str = Query(None),
    end_date: str = Query(None),
    status: str = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    pdf = generate_orders_report(db, start_date, end_date, status)
    return _pdf_response(pdf, "orders_report")


@router.get("/stock")
def stock_report(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    pdf = generate_stock_report(db)
    return _pdf_response(pdf, "stock_report")


@router.get("/ingredient-usage")
def usage_report(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    pdf = generate_usage_report(db, start_date, end_date)
    return _pdf_response(pdf, "ingredient_usage_report")


@router.get("/best-menu")
def best_menu_report(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    pdf = generate_best_menu_report(db, start_date, end_date)
    return _pdf_response(pdf, "best_menu_report")


@router.get("/activities")
def activity_report(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    pdf = generate_activity_report(db, start_date, end_date)
    return _pdf_response(pdf, "activity_report")
