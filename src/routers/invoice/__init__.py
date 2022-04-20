from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.core.dependencies import get_current_user, get_db
from src.models import Invoice
from src.schemas.invoice import CreateInvoice, ReadInvoice, UpdateInvoice
from src.schemas.user import CurrentUser

invoice_router = APIRouter(prefix="/invoice", tags=["invoice"])


@invoice_router.get(
    "",
    response_model=List[ReadInvoice],
)
def read_invoices(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    page: int = 1,
    page_size: int = 10,
):
    offset = (page - 1) * page_size
    limit = page * page_size
    stmt = (
        select(Invoice)
        .where(Invoice.user_id == current_user.id)
        .offset(offset)
        .limit(limit)
    )

    invoices = db.exec(stmt).all()

    return invoices


@invoice_router.get(
    "/{invoice_id}",
    response_model=ReadInvoice,
)
def read_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    stmt = (
        select(Invoice)
        .where(Invoice.id == invoice_id)
        .where(Invoice.user_id == current_user.id)
    )

    invoice = db.exec(stmt).first()

    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return invoice


@invoice_router.post(
    "",
    response_model=ReadInvoice,
)
def create_invoice(
    invoice: CreateInvoice,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    created_invoice = Invoice(**invoice.dict(), user_id=current_user.id)
    db.add(created_invoice)
    db.commit()
    db.refresh(created_invoice)

    return created_invoice


@invoice_router.put(
    "/{invoice_id}",
    response_model=ReadInvoice,
)
def update_invoice(
    invoice_id: int,
    invoice: UpdateInvoice,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    stmt = (
        select(Invoice)
        .where(Invoice.id == invoice_id)
        .where(Invoice.user_id == current_user.id)
    )

    invoice_to_update = db.exec(stmt).first()

    if invoice_to_update is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    invoice_to_update.title = invoice.title
    invoice_to_update.description = invoice.description
    invoice_to_update.amount = invoice.amount
    invoice_to_update.due_date = invoice.due_date

    db.add(invoice_to_update)
    db.commit()
    db.refresh(invoice_to_update)

    return invoice_to_update


@invoice_router.delete(
    "/{invoice_id}",
    status_code=204,
)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    stmt = (
        select(Invoice)
        .where(Invoice.id == invoice_id)
        .where(Invoice.user_id == current_user.id)
    )

    invoice_to_delete = db.exec(stmt).first()

    if invoice_to_delete is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice_to_delete)
    db.commit()
