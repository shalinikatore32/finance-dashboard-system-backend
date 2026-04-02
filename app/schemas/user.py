from pydantic import BaseModel, EmailStr, ConfigDict, Field
from enum import Enum
from datetime import datetime
from typing import Optional, Any

class RoleEnum(str, Enum):
    Admin = "Admin"
    Analyst = "Analyst"
    Viewer = "Viewer"

class UserBase(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    role: RoleEnum = RoleEnum.Viewer
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime
    
    model_config = ConfigDict(populate_by_name=True)

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
