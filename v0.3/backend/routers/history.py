from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from models.message import Message  # 引用消息模型
from schemas.message import MessageOut  # 引用消息模式
from models.database import get_db  # 假设有一个获取数据库会话的依赖

router = APIRouter()

# 数据模型
class SaveChatRequest(BaseModel):
    room_id: int
    user_id: int
    messages: List[MessageOut]

class RetrieveChatResponse(BaseModel):
    room_id: int
    messages: List[MessageOut]

# 接口：保存聊天记录
@router.post("/save")
async def save_chat(request: SaveChatRequest, db: Session = Depends(get_db)):
    for msg in request.messages:
        message = Message(
            room_id=request.room_id,
            user_id=request.user_id,
            content=msg.content,
            message_type=msg.message_type,
            status=msg.status,
            timestamp=datetime.now()  # 或者使用服务器时间
        )
        db.add(message)
    
    db.commit()
    # 同步到Elasticsearch（伪代码）
    # await elasticsearch_index_messages(request.messages)

    return {"status": "success", "message": "Chat history saved."}

# 接口：恢复聊天记录
@router.post("/retrieve", response_model=RetrieveChatResponse)
async def retrieve_chat(room_id: int, user_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter_by(room_id=room_id).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="No chat history found.")
    
    return RetrieveChatResponse(room_id=room_id, messages=messages)

# 接口：下载聊天记录
@router.get("/download/{room_id}")
async def download_chat(room_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter_by(room_id=room_id).all()
    
    if not messages:
        raise HTTPException(status_code=404, detail="No chat history found.")

    # 将消息转换为可下载格式（如JSON或CSV）
    # 此处省略具体实现细节
    return {"status": "success", "data": messages}  # 实际上可能需要返回文件链接或直接下载内容

# 接口：搜索聊天记录（可选）
@router.get("/search")
async def search_chat(room_id: int, keyword: str):
    # 从Elasticsearch中检索匹配的消息（伪代码）
    # results = await elasticsearch_search(room_id, keyword)
    
    return {
        "room_id": room_id,
        "filtered_messages": results  # 返回过滤后的消息列表
    }
