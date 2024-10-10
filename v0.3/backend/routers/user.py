# routers/user.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.user import User
from schemas.user import UserCreate, UserOut  # 导入Pydantic模型
from models.database import get_db
from utils.security import get_current_user, create_access_token

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    nickname: str = None
    avatar_url: str = None

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 注册逻辑：检查用户名和邮箱是否已存在，保存用户信息
    pass

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # 登录逻辑：验证用户身份，生成并返回JWT令牌
    pass

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # 登出逻辑：可以选择清除会话或标记为登出状态（如果使用JWT则无须此步骤）
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_user(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 更新用户信息逻辑
    pass

@router.put("/me/password")
def change_password(old_password: str, new_password: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 修改密码逻辑：验证旧密码，更新新密码
    pass

@router.delete("/me")
def delete_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 删除用户逻辑
    pass

@router.get("/oauth/{provider}")
def oauth_login(provider: str):
    # 第三方登录逻辑：重定向到OAuth提供商
    pass

@router.get("/oauth/callback")
def oauth_callback():
    # OAuth回调处理逻辑：获取用户信息并创建/返回用户对象
    pass

@router.get("/")
def list_users(current_user: User = Depends(get_current_user)):
    # 列出所有用户（仅限管理员）
    pass
