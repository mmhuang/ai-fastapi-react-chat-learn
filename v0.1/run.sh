#!/bin/bash
CHATROOM_PORT=${CHATROOM_PORT:-1999}
cd ../backend
uvicorn main:app --reload --port $CHATROOM_PORT --host 0.0.0.0