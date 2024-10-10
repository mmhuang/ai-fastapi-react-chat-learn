# routers/room.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Room, User 
from models.database import get_db
from schemas.room import RoomCreate, RoomOut
from utils.security import get_current_user

router = APIRouter()

@router.post("/rooms", response_model=RoomOut)
def create_room(room_create: RoomCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 创建新聊天室逻辑
    pass

@router.get("/rooms")
def list_rooms(db: Session = Depends(get_db)):
    # 获取聊天室列表逻辑
    pass

@router.post("/rooms/{room_id}/join")
def join_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 用户加入聊天室逻辑
    pass

@router.post("/rooms/{room_id}/leave")
def leave_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 用户离开聊天室逻辑
    pass

@router.get("/rooms/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    # 获取指定聊天室信息逻辑
    pass

@router.put("/rooms/{room_id}")
def update_room(room_id: int, room_update: RoomCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 更新聊天室信息逻辑
    pass

@router.delete("/rooms/{room_id}")
def delete_room(room_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 删除聊天室逻辑，仅限管理员
    pass

@router.post("/rooms/{room_id}/members/{user_id}/kick")
def kick_member(room_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 踢出成员逻辑，仅限管理员
    pass

@router.post("/rooms/{room_id}/members/{user_id}/mute")
def mute_member(room_id: int, user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 禁言成员逻辑，仅限管理员
    pass
