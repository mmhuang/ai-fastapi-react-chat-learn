# schemas/room.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_members: Optional[int] = 100
    is_private: Optional[bool] = False

class RoomCreate(RoomBase):
    pass

class RoomOut(RoomBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
