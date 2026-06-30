import io
from datetime import date, datetime, timezone
from typing import Optional

from fpdf import FPDF
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.models.stock_transaction import StockTransaction
from app.models.user import User

RESTAURANT_NAME = "WorldPlate"
LOGO_PATH = "storage/logo.png"


class ReportPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_watermark(self):
        self.set_font("Helvetica", "B", 60)
        self.set_text_color(210, 210, 210)
        self.rotate_text(-45, 105, 140, f"{RESTAURANT_NAME} - Confidential")

    def rotate_text(self, angle, x, y, txt):
        with self.rotation(angle, x, y):
            self.set_xy(x - 50, y - 20)
            self.cell(100, 10, txt, align="C")

    def report_title(self, title: str, subtitle: str = ""):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(50, 50, 50)
        self.cell(0, 9, title, align="L", new_x="LMARGIN", new_y="NEXT")
        if subtitle:
            self.set_font("Helvetica", "", 9)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, subtitle, align="L", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(1.5)

    def table_header(self, cols: list[str], widths: list[int]):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(220, 100, 10)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cols: list[str], widths: list[int], align: list[str] | None = None, fill: bool = False):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(40, 40, 40)
        if fill:
            self.set_fill_color(248, 248, 248)
        max_lines = 1
        cell_lines = []
        for i, col in enumerate(cols):
            lines = self.multi_cell(widths[i], 5, str(col), split_only=True)
            cell_lines.append(lines)
            max_lines = max(max_lines, len(lines))

        row_h = max_lines * 5
        x_start = self.get_x()
        y_start = self.get_y()

        for i, col in enumerate(cols):
            x = x_start + sum(widths[:i])
            self.set_xy(x, y_start)
            a = (align[i] if align else "L") if len(widths) > 0 else "L"
            self.multi_cell(widths[i], 5, str(col), border=1, align=a, fill=fill)

        self.set_xy(x_start, y_start + row_h)

    def simple_row(self, cols: list[str], widths: list[int], align: list[str] | None = None, fill: bool = False):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(40, 40, 40)
        if fill:
            self.set_fill_color(248, 248, 248)
        for i, col in enumerate(cols):
            a = (align[i] if align else "L") if align else "L"
            self.cell(widths[i], 7, str(col), border=1, align=a, fill=fill)
        self.ln()

    def empty_row(self, widths: list[int], message: str = "No data available"):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(140, 140, 140)
        self.cell(sum(widths), 7, message, border=1, align="C")
        self.ln()


def _parse_date(date_str: Optional[str]) -> Optional[date]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def _add_logo(pdf: ReportPDF):
    import os
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=pdf.w - pdf.r_margin - 25, y=8, w=25)


def generate_sales_report(db: Session, start_date: Optional[str], end_date: Optional[str]) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    _add_logo(pdf)
    pdf.add_watermark()

    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    query = db.query(
        func.date(Order.created_at).label("day"),
        func.count(Order.id).label("order_count"),
        func.sum(Order.total_price).label("revenue"),
    ).filter(
        Order.status != "cancelled"
    )
    if sd:
        query = query.filter(func.date(Order.created_at) >= sd)
    if ed:
        query = query.filter(func.date(Order.created_at) <= ed)
    query = query.group_by(func.date(Order.created_at)).order_by(func.date(Order.created_at))

    rows = query.all()
    total_revenue = sum(float(r.revenue or 0) for r in rows)
    total_orders = sum(r.order_count for r in rows)

    subtitle = f"Period: {start_date or ' earliest'} - {end_date or ' today'}"
    pdf.report_title("Sales Report", subtitle)

    if total_orders > 0:
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(0, 7, f"Total Revenue: Rp {total_revenue:,.0f}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, f"Total Orders: {total_orders}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    widths = [40, 40, 60, 40]
    pdf.table_header(["Date", "Orders", "Revenue", "Avg/Order"], widths)

    if not rows:
        pdf.empty_row(widths)
    else:
        for i, r in enumerate(rows):
            day_str = r.day.strftime("%d %b %Y") if r.day else "-"
            avg = float(r.revenue or 0) / r.order_count if r.order_count else 0
            pdf.simple_row(
                [day_str, str(r.order_count), f"Rp {float(r.revenue or 0):,.0f}", f"Rp {avg:,.0f}"],
                widths,
                align=["L", "C", "R", "R"],
                fill=i % 2 == 0,
            )

    return pdf.output()


def generate_orders_report(db: Session, start_date: Optional[str], end_date: Optional[str], status_filter: Optional[str] = None) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    _add_logo(pdf)
    pdf.add_watermark()

    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    query = db.query(Order)
    if sd:
        query = query.filter(func.date(Order.created_at) >= sd)
    if ed:
        query = query.filter(func.date(Order.created_at) <= ed)
    if status_filter:
        query = query.filter(Order.status == status_filter)
    query = query.order_by(Order.created_at.desc()).limit(200)

    orders = query.all()

    subtitle = f"Period: {start_date or 'earliest'} - {end_date or 'today'}"
    pdf.report_title("Orders Report", subtitle)

    widths = [22, 30, 50, 24, 30, 34]
    pdf.table_header(["#", "Date", "Customer", "Status", "Payment", "Total"], widths)

    if not orders:
        pdf.empty_row(widths)
    else:
        for i, o in enumerate(orders):
            customer_name = o.user.full_name if o.user else "-"
            pdf.simple_row(
                [
                    o.order_number or str(o.id),
                    o.created_at.strftime("%d/%m/%Y") if o.created_at else "-",
                    customer_name[:20],
                    o.status.capitalize(),
                    o.payment_status.capitalize(),
                    f"Rp {float(o.total_price):,.0f}",
                ],
                widths,
                align=["L", "L", "L", "C", "C", "R"],
                fill=i % 2 == 0,
            )

    return pdf.output()


def generate_stock_report(db: Session) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    _add_logo(pdf)
    pdf.add_watermark()

    pdf.report_title("Stock Report", f"As of {datetime.now(timezone.utc).strftime('%d %b %Y %H:%M')} UTC")

    ingredients = db.query(Ingredient).filter(Ingredient.is_active == True).order_by(Ingredient.name).all()

    widths = [60, 25, 25, 25, 25, 30]
    pdf.table_header(["Ingredient", "SKU", "Unit", "Stock", "Min Stock", "Status"], widths)

    if not ingredients:
        pdf.empty_row(widths)
    else:
        for i, ing in enumerate(ingredients):
            status = "Low Stock" if float(ing.stock_qty) <= float(ing.min_stock) else "OK"
            pdf.simple_row(
                [ing.name, ing.sku or "-", ing.unit, str(float(ing.stock_qty)), str(float(ing.min_stock)), status],
                widths,
                align=["L", "L", "C", "C", "C", "C"],
                fill=i % 2 == 0,
            )

    return pdf.output()


def generate_usage_report(db: Session, start_date: Optional[str], end_date: Optional[str]) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    _add_logo(pdf)
    pdf.add_watermark()

    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    query = db.query(StockTransaction).filter(StockTransaction.type == "OUT")
    if sd:
        query = query.filter(func.date(StockTransaction.created_at) >= sd)
    if ed:
        query = query.filter(func.date(StockTransaction.created_at) <= ed)
    query = query.order_by(StockTransaction.created_at.desc()).limit(200)

    txns = query.all()

    subtitle = f"Period: {start_date or 'earliest'} - {end_date or 'today'}"
    pdf.report_title("Ingredient Usage Report", subtitle)

    widths = [50, 25, 25, 30, 50]
    pdf.table_header(["Ingredient", "Qty", "Unit", "Reference", "Date"], widths)

    if not txns:
        pdf.empty_row(widths)
    else:
        for i, t in enumerate(txns):
            ing_name = t.ingredient.name if t.ingredient else "-"
            pdf.simple_row(
                [
                    ing_name[:25],
                    str(float(t.qty)),
                    t.ingredient.unit if t.ingredient else "-",
                    t.reference_type or "-",
                    t.created_at.strftime("%d/%m/%Y") if t.created_at else "-",
                ],
                widths,
                align=["L", "C", "C", "L", "L"],
                fill=i % 2 == 0,
            )

    return pdf.output()


def generate_best_menu_report(db: Session, start_date: Optional[str], end_date: Optional[str]) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    _add_logo(pdf)
    pdf.add_watermark()

    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    query = db.query(
        MenuItem.id,
        MenuItem.name,
        func.sum(OrderItem.qty).label("total_qty"),
        func.sum(OrderItem.subtotal).label("total_revenue"),
    ).join(OrderItem, OrderItem.menu_item_id == MenuItem.id)\
     .join(Order, Order.id == OrderItem.order_id)\
     .filter(Order.status != "cancelled")

    if sd:
        query = query.filter(func.date(Order.created_at) >= sd)
    if ed:
        query = query.filter(func.date(Order.created_at) <= ed)

    query = query.group_by(MenuItem.id, MenuItem.name)\
                 .order_by(func.sum(OrderItem.qty).desc())\
                 .limit(50)

    rows = query.all()

    subtitle = f"Period: {start_date or 'earliest'} - {end_date or 'today'}"
    pdf.report_title("Best Selling Menu Report", subtitle)

    widths = [10, 70, 30, 30, 50]
    pdf.table_header(["#", "Menu Item", "Qty Sold", "Revenue", "Avg Price/Item"], widths)

    if not rows:
        pdf.empty_row(widths)
    else:
        for idx, r in enumerate(rows):
            avg_price = float(r.total_revenue or 0) / r.total_qty if r.total_qty else 0
            pdf.simple_row(
                [
                    str(idx + 1),
                    r.name[:35],
                    str(r.total_qty),
                    f"Rp {float(r.total_revenue or 0):,.0f}",
                    f"Rp {avg_price:,.0f}",
                ],
                widths,
                align=["C", "L", "C", "R", "R"],
                fill=idx % 2 == 0,
            )

    return pdf.output()


def generate_activity_report(db: Session, start_date: Optional[str], end_date: Optional[str]) -> bytes:
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    _add_logo(pdf)
    pdf.add_watermark()

    sd = _parse_date(start_date)
    ed = _parse_date(end_date)

    query = db.query(StockTransaction).join(User, StockTransaction.created_by == User.id, isouter=True)
    if sd:
        query = query.filter(func.date(StockTransaction.created_at) >= sd)
    if ed:
        query = query.filter(func.date(StockTransaction.created_at) <= ed)
    query = query.order_by(StockTransaction.created_at.desc()).limit(200)

    txns = query.all()

    subtitle = f"Period: {start_date or 'earliest'} - {end_date or 'today'}"
    pdf.report_title("Activity Report", subtitle)

    widths = [25, 45, 25, 25, 60]
    pdf.table_header(["Date", "User", "Type", "Ingredient", "Notes"], widths)

    if not txns:
        pdf.empty_row(widths)
    else:
        for i, t in enumerate(txns):
            user_name = t.created_by_user.full_name if t.created_by_user else "-"
            ing_name = t.ingredient.name if t.ingredient else "-"
            pdf.simple_row(
                [
                    t.created_at.strftime("%d/%m/%Y") if t.created_at else "-",
                    user_name[:22],
                    t.type,
                    ing_name[:22],
                    (t.notes or "-")[:30],
                ],
                widths,
                align=["L", "L", "C", "L", "L"],
                fill=i % 2 == 0,
            )

    return pdf.output()
