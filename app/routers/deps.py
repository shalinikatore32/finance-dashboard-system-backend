from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app.core.config import settings
from app.core.security import oauth2_scheme
from app.db.mongodb import get_users_collection
from app.schemas.user import UserResponse, RoleEnum
from bson import ObjectId

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    users_collection = get_users_collection()
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    
    # Map _id to id for UserResponse
    user["id"] = str(user["_id"])
    
    if not user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return UserResponse(**user)

def require_role(allowed_roles: list[RoleEnum]):
    async def role_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker

# Predefined dependencies
RequireAdmin = Depends(require_role([RoleEnum.Admin]))
RequireAnalyst = Depends(require_role([RoleEnum.Admin, RoleEnum.Analyst]))
RequireViewer = Depends(require_role([RoleEnum.Admin, RoleEnum.Analyst, RoleEnum.Viewer]))
