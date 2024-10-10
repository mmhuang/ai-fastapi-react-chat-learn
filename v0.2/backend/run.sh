#!/bin/bash

test -f .env && source .env

CHATROOM_PORT=${CHATROOM_PORT:-1999}
cd app
uvicorn main:app --reload --port $CHATROOM_PORT --host 0.0.0.0