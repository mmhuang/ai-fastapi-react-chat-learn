from fastapi import Depends, FastAPI
from backend.dependencies import get_current_user

app = FastAPI()

@app.get("/status")
async def read_status(current_user: dict = Depends(get_current_user)):
    return {"status": "up", "current_user": current_user}