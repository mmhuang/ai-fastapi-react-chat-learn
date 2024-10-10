# models/file.py

from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_url = Column(String(255), nullable=False)
    file_type = Column(Enum('image', 'document', 'video'), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')

    user = relationship('User', back_populates='files')
