from fastapi import APIRouter, Depends
from typing import List
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import create_user, update_user, get_all_users
from app.routers.deps import RequireAdmin, RequireAnalyst, RequireViewer, get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_new_user(user_in: UserCreate, current_user: UserResponse = RequireAdmin):
    """Create a new user. Admin only."""
    return await create_user(user_in)

@router.get("/", response_model=List[UserResponse])
async def list_users(current_user: UserResponse = RequireAdmin):
    """List all users. Admin only."""
    return await get_all_users()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user."""
    return current_user

@router.patch("/{user_id}", response_model=UserResponse)
async def update_existing_user(user_id: str, user_in: UserUpdate, current_user: UserResponse = RequireAdmin):
    """Update user role or status. Admin only."""
    return await update_user(user_id, user_in)
