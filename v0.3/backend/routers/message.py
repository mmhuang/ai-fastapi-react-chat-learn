from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class MessageType(str, Enum):
    text = 'text'
    image = 'image'
    file = 'file'
    markdown = 'markdown'

class MessageStatus(str, Enum):
    sent = 'sent'
    delivered = 'delivered'
    read = 'read'

class MessageBase(BaseModel):
    content: str
    message_type: MessageType
    status: MessageStatus

class MessageCreate(MessageBase):
    room_id: int  # 房间ID
    user_id: int  # 用户ID

class Message(MessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True  # 支持从ORM模型转换为Pydantic模型
