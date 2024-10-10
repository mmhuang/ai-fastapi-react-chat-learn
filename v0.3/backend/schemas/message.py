# schemas/message.py

from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    message_type: Literal['text', 'image', 'file', 'markdown']
    status: Literal['sent', 'delivered', 'read'] = 'sent'

class MessageCreate(MessageBase):
    room_id: int
    user_id: int

class MessageOut(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
