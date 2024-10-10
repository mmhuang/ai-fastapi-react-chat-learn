# schemas/file.py

from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class FileBase(BaseModel):
    file_url: str
    file_type: Literal['image', 'document', 'video']

class FileCreate(FileBase):
    user_id: int

class FileOut(FileBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
