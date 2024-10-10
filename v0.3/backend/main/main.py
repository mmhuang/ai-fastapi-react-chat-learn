# main/server.py

from fastapi import FastAPI
from routers import user, room, file, community, chat, history

app = FastAPI()

# 注册路由
app.include_router(user.router, prefix="/users")
app.include_router(room.router, prefix="/rooms")
app.include_router(file.router, prefix="/files")
app.include_router(history.router, prefix="/histories")
app.include_router(community.router, prefix="/communities")
app.include_router(chat.router, prefix="/chat")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
