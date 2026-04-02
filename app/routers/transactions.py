from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import datetime
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import create_transaction, get_transactions, update_transaction, delete_transaction
from app.routers.deps import RequireAdmin, RequireAnalyst, RequireViewer

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
async def create_new_transaction(
    transaction_in: TransactionCreate, 
    current_user = RequireAdmin
):
    """Create a transaction. Admin only."""
    return await create_transaction(transaction_in, current_user.id)

@router.get("/")
async def list_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user = RequireViewer
):
    """List transactions with pagination and filtering. Accessible by all roles."""
    return await get_transactions(
        page=page, 
        limit=limit, 
        search=search, 
        category=category, 
        type=type, 
        start_date=start_date, 
        end_date=end_date
    )

@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_existing_transaction(
    transaction_id: str, 
    transaction_in: TransactionUpdate, 
    current_user = RequireAdmin
):
    """Update a transaction. Admin only."""
    return await update_transaction(transaction_id, transaction_in)

@router.delete("/{transaction_id}")
async def soft_delete_transaction(
    transaction_id: str, 
    current_user = RequireAdmin
):
    """Soft delete a transaction. Admin only."""
    return await delete_transaction(transaction_id)
