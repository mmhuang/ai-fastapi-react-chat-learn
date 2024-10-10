# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 数据库连接字符串
DATABASE_URL = "sqlite:///chat.db"  # 根据你的数据库调整
# DATABASE_URL = "mysql+pymysql://username:password@localhost/db_name"  # 根据你的数据库调整

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建基础类
Base = declarative_base()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 获取会话实例的函数
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
