from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional

class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: TransactionType
    category: str
    date: datetime
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    notes: Optional[str] = None

class TransactionInDB(TransactionBase):
    id: str = Field(alias="_id")
    created_by: str  # User ID
    created_at: datetime
    is_deleted: bool = False

    model_config = ConfigDict(populate_by_name=True)

class TransactionResponse(TransactionBase):
    id: str
    created_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
