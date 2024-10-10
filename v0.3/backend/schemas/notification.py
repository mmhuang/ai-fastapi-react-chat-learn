from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationCreateRequest(BaseModel):
    user_id: int
    content: str
    notification_type: str  # 'message', 'system', 'reminder'

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    content: str
    notification_type: str
    is_read: bool
    timestamp: datetime

    class Config:
        orm_mode = True  # 允许从ORM模型转换为Pydantic模型
