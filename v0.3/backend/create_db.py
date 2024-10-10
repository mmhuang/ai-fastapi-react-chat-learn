# create_db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

DATABASE_URL = "sqlite:///chat.db"

engine = create_engine(DATABASE_URL)

if not os.path.exists("chat.db"):
    Base.metadata.create_all(engine)
