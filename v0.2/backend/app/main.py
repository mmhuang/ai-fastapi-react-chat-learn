# main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware  # 导入 CORS 中间件
from typing import List

app = FastAPI()

# 添加 CORS 中间件
origins = [
    "http://localhost:1999",  # 你的前端 URL
    "http://localhost:8001",   # 如果有其他允许的源，可以添加到这里
    "http://10.126.3.80:8001",   # 如果有其他允许的源，可以添加到这里
    "*",  # 允许所有来源（不推荐用于生产环境）
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)



# 用于存储活跃 WebSocket 连接的列表
active_connections: List[WebSocket] = []

# 主页路由
@app.get("/", response_class=HTMLResponse)
async def get():
    return HTMLResponse(open("static/chat.html").read())

# 处理 WebSocket 连接
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 向所有连接的客户端发送消息
            for connection in active_connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# 运行命令
# uvicorn main:app --reload
