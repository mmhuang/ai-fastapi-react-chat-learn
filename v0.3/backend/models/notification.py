from sqlalchemy import Column, Integer, Text, Enum, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    notification_type = Column(Enum('message', 'system', 'reminder'), nullable=False)
    is_read = Column(Boolean, default=False)
    timestamp = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    # 反向关系（可选）
    user = relationship('User', back_populates='notifications')
