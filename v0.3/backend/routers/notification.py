from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from models.notification import Notification  # 引用通知模型
from models.database import get_db  # 假设有一个获取数据库会话的依赖

router = APIRouter()

# 数据模型
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
    timestamp: str

# 接口：创建新通知
@router.post("/create", response_model=NotificationResponse)
async def create_notification(request: NotificationCreateRequest, db: Session = Depends(get_db)):
    notification = Notification(
        user_id=request.user_id,
        content=request.content,
        notification_type=request.notification_type,
        is_read=False
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)  # 获取最新的通知数据
    
    return notification

# 接口：获取用户通知列表
@router.get("/{user_id}", response_model=List[NotificationResponse])
async def get_notifications(user_id: int, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter_by(user_id=user_id).all()
    
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found.")
    
    return notifications

# 接口：标记通知为已读
@router.put("/read/{notification_id}")
async def mark_as_read(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter_by(id=notification_id).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found.")
    
    notification.is_read = True
    db.commit()
    
    return {"status": "success", "message": "Notification marked as read."}

# 接口：删除通知（可选）
@router.delete("/{notification_id}")
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(Notification).filter_by(id=notification_id).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found.")
    
    db.delete(notification)
    db.commit()
    
    return {"status": "success", "message": "Notification deleted."}
