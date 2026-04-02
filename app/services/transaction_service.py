from bson import ObjectId
from datetime import datetime
from typing import Optional
from app.db.mongodb import get_transactions_collection
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from fastapi import HTTPException, status
import re

async def create_transaction(transaction_in: TransactionCreate, user_id: str):
    transactions_collection = get_transactions_collection()
    transaction_dict = transaction_in.model_dump()
    transaction_dict["created_by"] = user_id
    transaction_dict["created_at"] = datetime.utcnow()
    transaction_dict["is_deleted"] = False
    
    result = await transactions_collection.insert_one(transaction_dict)
    transaction_dict["id"] = str(result.inserted_id)
    return transaction_dict

async def get_transactions(
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    transactions_collection = get_transactions_collection()
    
    # Base query excludes soft deleted items
    query = {"is_deleted": False}
    
    # Filtering
    if search:
        query["$or"] = [
            {"notes": {"$regex": re.compile(search, re.IGNORECASE)}},
            {"category": {"$regex": re.compile(search, re.IGNORECASE)}}
        ]
    if category:
        query["category"] = category
    if type:
        query["type"] = type
    
    # Date filtering
    if start_date or end_date:
        query["date"] = {}
        if start_date:
            query["date"]["$gte"] = start_date
        if end_date:
            query["date"]["$lte"] = end_date
            
    skip = (page - 1) * limit
    
    cursor = transactions_collection.find(query).sort("date", -1).skip(skip).limit(limit)
    total_count = await transactions_collection.count_documents(query)
    
    transactions = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        transactions.append(doc)
        
    return {
        "data": transactions,
        "total": total_count,
        "page": page,
        "limit": limit
    }

async def update_transaction(transaction_id: str, transaction_in: TransactionUpdate):
    transactions_collection = get_transactions_collection()
    update_data = {k: v for k, v in transaction_in.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
        
    result = await transactions_collection.update_one(
        {"_id": ObjectId(transaction_id), "is_deleted": False},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found or deleted")
        
    updated = await transactions_collection.find_one({"_id": ObjectId(transaction_id)})
    updated["id"] = str(updated["_id"])
    return updated

async def delete_transaction(transaction_id: str):
    transactions_collection = get_transactions_collection()
    # Soft delete
    result = await transactions_collection.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": {"is_deleted": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        
    return {"message": "Transaction logically deleted successfully"}
