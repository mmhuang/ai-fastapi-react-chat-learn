#!/bin/bash

# 创建项目根目录
PROJECT_NAME="MyAwesomeProject"
mkdir $PROJECT_NAME
cd $PROJECT_NAME

# 创建后端目录结构
echo "Creating backend directory structure..."
mkdir backend
cd backend
mkdir main
mkdir -p models schemas
mkdir -p routers/auth routers/items
touch main/__init__.py main/server.py models/__init__.py schemas/__init__.py
echo "from fastapi import FastAPI" > main/server.py
echo "app = FastAPI()" >> main/server.py
echo "# Import routers here" >> main/server.py
cd ..

# 创建前端目录结构
echo "Creating frontend directory structure..."
mkdir frontend
cd frontend
echo "Creating React app..."
npx create-react-app .
echo "Installing Ant Design..."
npm install antd
cd ..

# 创建其他通用文件
echo "Creating other common files..."
touch README.md .gitignore
echo "# $PROJECT_NAME" > README.md
echo "# (.gitignore will be configured later)"

echo "Project directory structure created successfully!"