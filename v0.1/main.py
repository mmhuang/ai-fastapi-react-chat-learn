# Chatroom Backend Service using FastAPI

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

import json
import os
import logging
import dotenv
import yaml

# load environment variables
dotenv.load_dotenv()

# load configuration from config.yaml
config = {}
with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

app = FastAPI()
logging.basicConfig(level=logging.INFO)

clients = {}

@app.get("/chat")
def get():
    # load cookie
    # if user_name is None, redirect to login
    request = Request()
    cookie = request.cookies.get("user_name")
    if cookie is None:
        return RedirectResponse(url="/login")
    
    return _load_html("main.html")

@app.post("/chat")
async def post(request: Request):
     
    cookie = request.cookies.get("user_name")
    if cookie is None:
        return RedirectResponse(url="/login")
    
    return _load_html("chat.html")    


session_count = 0

@app.websocket("/ws/chatroom")

async def chatroom(websocket: WebSocket):


    await websocket.accept()
    # generate random session name and store it in the websocket client; 
    # update session count; 
    # broadcast the session count

    # get cookie
    user_name = websocket.cookies.get("user_name")


    global session_count
    websocket.client_name = f"client_{user_name}"
    session_count += 1
    await websocket.send_text(f"You are connected: {websocket.client_name}")
    broadcast(f"New client connected: {websocket.client_name}")
    clients[websocket] = True
    logging.info("Session created: %s", websocket.client_name)

    try:
        while True:
            data = await websocket.receive_text()
            logging.info("Received message: %s", data)
            await broadcast(websocket.client_name+":"+data)
    except WebSocketDisconnect:
        # broadcast the disconnection message
        # await broadcast(f"Client {websocket.client} left the chatroom")
        del clients[websocket]
        logging.info("Client disconnected: %s", websocket.client)

async def broadcast(message: str):
    for client in clients:
        await client.send_text(message)
        logging.info("Broadcast message: %s", message)



@app.get("/")
async def read_root():
    return _load_html("index.html")

@app.get("/register")
def register(request: Request):
    return _load_html("register.html")


@app.post("/register")
async def register_user(user_name: str = Form(None), password: str = Form(None)):

    logging.info("Register user: %s", user_name)
    
    users = {}
    with open('.pass.json', 'r') as f:
        users = json.load(f)
        if user_name in users:
            return _load_html("register_error.html")

    users[user_name] = password

    with open('.pass.json', 'w') as f:
        json.dump(users, f)

    # redirect to login
    response = RedirectResponse(url='/login')
    return response
    

@app.get("/login")
async def login(request: Request):
    return _load_html("login.html")


@app.post("/login")
async def login_user(request: Request):
    my_form = await request.form()
    user_name = my_form["user_name"]
    password = my_form["password"]
    with open('.pass.json', 'r') as f:
        users = json.load(f)
        if user_name not in users or users[user_name] != password:
            return _load_html("login_error.html")
    # redirect to chatroom
    response = RedirectResponse(url='/chat')
    response.set_cookie(key="user_name", value=user_name)
    return response

def _load_html(file_name):
    html_file = os.path.join(config["service_config"]["html_dir"], file_name)
    with open(html_file) as f:
        return HTMLResponse(f.read())