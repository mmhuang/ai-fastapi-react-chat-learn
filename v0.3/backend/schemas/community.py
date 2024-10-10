# schemas/community.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommunityBase(BaseModel):
    name: str
    description: Optional[str] = None
    rules: Optional[str] = None

class CommunityCreate(CommunityBase):
    pass

class CommunityOut(CommunityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
