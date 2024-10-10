from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import openai
import json
from models.chat_log import ChatLog
from models.database import get_db

router = APIRouter()

class UserMessageRequest(BaseModel):
    user_id: int
    message: str

class BotResponse(BaseModel):
    response: str

def extract_context(message: str) -> dict:
    # 简单示例：从消息中提取特定关键字或上下文
    keywords = ["urgent", "important"]  # 假设这是要提取的关键字
    context = {keyword: keyword in message for keyword in keywords}
    return context

@router.post("/message", response_model=BotResponse)
async def process_message(request: UserMessageRequest, db: Session = Depends(get_db)):
    try:
        # 提取上下文信息
        context = extract_context(request.message)

        # 调用 AI 聊天机器人 API，并传入上下文
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": request.message},
                {"role": "system", "content": json.dumps(context)}  # 将上下文传递给模型
            ]
        )
        
        bot_reply = ai_response['choices'][0]['message']['content']
        
        # 保存聊天记录到数据库，包括上下文信息
        chat_log = ChatLog(
            user_id=request.user_id,
            message=request.message,
            bot_response=bot_reply,
            context=json.dumps(context)  # 存储上下文为 JSON 字符串
        )
        
        db.add(chat_log)
        db.commit()
        db.refresh(chat_log)
        
        return {"response": bot_reply}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
