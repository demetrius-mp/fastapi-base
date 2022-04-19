from fastapi import APIRouter

from .auth import auth_router
from .invoice import invoice_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(invoice_router)
