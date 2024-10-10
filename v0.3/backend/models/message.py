# models/message.py

from sqlalchemy import Column, ForeignKey, Integer, Text, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
    message_type = Column(Enum('text', 'image', 'file', 'markdown'), nullable=False)
    status = Column(Enum('sent', 'delivered', 'read'), default='sent')
    timestamp = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    room = relationship('Room', back_populates='messages')
    user = relationship('User', back_populates='messages')
