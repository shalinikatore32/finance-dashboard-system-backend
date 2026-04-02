from bson import ObjectId
from datetime import datetime
from app.db.mongodb import get_users_collection
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from fastapi import HTTPException, status

async def get_user_by_email(email: str):
    users_collection = get_users_collection()
    return await users_collection.find_one({"email": email})

async def get_user_by_id(user_id: str):
    users_collection = get_users_collection()
    return await users_collection.find_one({"_id": ObjectId(user_id)})

async def create_user(user_in: UserCreate):
    users_collection = get_users_collection()
    existing_user = await get_user_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user_dict = user_in.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = datetime.utcnow()
    
    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return user_dict

async def update_user(user_id: str, user_in: UserUpdate):
    users_collection = get_users_collection()
    update_data = {k: v for k, v in user_in.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
        
    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    updated_user = await get_user_by_id(user_id)
    updated_user["id"] = str(updated_user["_id"])
    return updated_user

async def get_all_users():
    users_collection = get_users_collection()
    users = []
    async for user in users_collection.find():
        user["id"] = str(user["_id"])
        users.append(user)
    return users
