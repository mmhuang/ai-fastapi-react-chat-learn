# models/community.py

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from .base import Base

class Community(Base):
    __tablename__ = 'communities'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    rules = Column(Text)
    created_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    members = relationship('CommunityMember', back_populates='community')
