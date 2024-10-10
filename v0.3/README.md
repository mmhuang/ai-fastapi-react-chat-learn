# MyAwesomeProject
.
├── main
│   ├── __init__.py
│   └── server.py            # 启动应用的主文件
├── models                    # 数据库模型定义
│   ├── __init__.py
│   ├── base.py              # 基础模型类（如SQLAlchemy的Base）
│   ├── user.py              # 用户模型
│   ├── room.py              # 聊天室模型
│   ├── message.py           # 消息模型
│   ├── file.py              # 文件模型
│   └── community.py          # 社群模型
├── schemas                   # Pydantic模式定义
│   ├── __init__.py
│   ├── user.py              # 用户输入/输出模式
│   ├── room.py              # 聊天室输入/输出模式
│   ├── message.py           # 消息输入/输出模式
│   ├── file.py              # 文件输入/输出模式
│   └── community.py         # 社群输入/输出模式
├── routers                   # API路由定义
│   ├── __init__.py
│   ├── user.py              # 用户相关API路由
│   ├── room.py              # 聊天室管理的API路由
│   ├── chat.py              # 聊天室API路由（基于websock）
│   ├── file.py              # 文件上传/下载相关API路由
│   └── community.py         # 社群相关API路由
├── utils                     # 工具函数和辅助模块
│   ├── __init__.py
│   ├── security.py          # 安全性相关工具（如密码哈希）
│   └── notifications.py      # 通知发送工具
├── tests                     # 单元测试目录
│   ├── test_user.py         # 用户相关测试
│   ├── test_chat.py         # 聊天室相关测试
│   ├── test_file.py         # 文件相关测试
│   └── test_community.py     # 社群相关测试
├── alembic                   # 数据库迁移工具配置
│   ├── versions              # 版本迁移脚本存放目录
│   ├── env.py               # Alembic环境配置文件
│   ├── README                # Alembic使用说明
│   └── script.py.mako       # 脚本模板
├── create_db.py             # 初始化数据库的脚本
├── dependencies.py           # 依赖项管理（如FastAPI的依赖注入）
├── config.py                 # 配置文件管理（如数据库连接、API密钥等）
├── requirements.txt          # Python依赖包列表
├── Dockerfile                # Docker构建文件
├── .dockerignore             # Docker忽略文件列表
├── .gitignore                # Git忽略文件列表
├── .env                      # 环境变量文件（生产环境）
├── .env.dev                  # 开发环境变量文件
├── .env.prod                 # 生产环境变量文件
├── .env.test                 # 测试环境变量文件
└── README.md                 # 项目说明文档


数据库的设计如下：

旧：
CREATE TABLE users (
id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash VARCHAR(255) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
avatar_url VARCHAR(255),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

新：
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    avatar_url VARCHAR(255),
    nickname VARCHAR(50),  -- 新增昵称字段
    role ENUM('user', 'admin') DEFAULT 'user',  -- 用户角色
    provider VARCHAR(50),  -- 第三方登录提供者 (如 Google, Facebook)
    provider_id VARCHAR(100),  -- 第三方账号 ID
    status ENUM('active', 'inactive') DEFAULT 'active',  -- 用户状态
    privacy_policy_accepted_at TIMESTAMP,  -- 同意隐私政策的时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

聊天室表 (rooms)

CREATE TABLE rooms (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
description TEXT,
max_members INT DEFAULT 100,
is_private BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

新的：
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    max_members INT DEFAULT 100,
    is_private BOOLEAN DEFAULT FALSE,
    creator_id INT REFERENCES users(id),  -- 创建者 ID
    status ENUM('active', 'inactive') DEFAULT 'active',  -- 聊天室状态
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


聊天室成员表 (room_members)

CREATE TABLE room_members (
id SERIAL PRIMARY KEY,
room_id INT REFERENCES rooms(id),
user_id INT REFERENCES users(id),
role ENUM('admin', 'member') DEFAULT 'member',
joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

新的
CREATE TABLE room_members (
    id SERIAL PRIMARY KEY,
    room_id INT REFERENCES rooms(id),
    user_id INT REFERENCES users(id),
    role ENUM('admin', 'member') DEFAULT 'member',
    status ENUM('active', 'muted') DEFAULT 'active',  -- 成员状态
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


消息表 (messages)

CREATE TABLE messages (
id SERIAL PRIMARY KEY,
room_id INT REFERENCES rooms(id),
user_id INT REFERENCES users(id),
content TEXT,
message_type ENUM('text', 'image', 'file', 'markdown') NOT NULL,
status ENUM('sent', 'delivered', 'read') DEFAULT 'sent',
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
文件表 (files)

CREATE TABLE files (
id SERIAL PRIMARY KEY,
user_id INT REFERENCES users(id),
file_url VARCHAR(255) NOT NULL,
file_type ENUM('image', 'document', 'video') NOT NULL,
uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
社群表 (communities)

CREATE TABLE communities (
id SERIAL PRIMARY KEY,
name VARCHAR(100) NOT NULL,
description TEXT,
rules TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
社群成员表 (community_members)

CREATE TABLE community_members (
id SERIAL PRIMARY KEY,
community_id INT REFERENCES communities(id),
user_id INT REFERENCES users(id),
role ENUM('admin', 'member') DEFAULT 'member',
joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    content TEXT NOT NULL,
    notification_type ENUM('message', 'system', 'reminder') NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


1. 聊天室消息协议设计
在使用 gifted-chat 时，消息通常包含以下字段：

id: 消息唯一标识符
text: 消息内容
user: 发送者信息（包括用户ID和名称）
createdAt: 消息创建时间
image: 图片URL（可选）
file: 文件相关信息（可选）
基于此，我们可以定义一个更详细的消息协议：

```
{
  "id": "unique-message-id",
  "text": "Hello, world!",
  "user": {
    "id": "user-id",
    "name": "User Name",
    "avatar": "http://example.com/avatar.jpg"
  },
  "createdAt": "2024-10-06T12:34:56Z",
  "image": "http://example.com/image.jpg", // 可选
  "file": {
    "url": "http://example.com/file.pdf",
    "type": "document" // 可选
  }
}
```

功能设计

- 用户管理
用户注册、登录、登出：提供基本的用户账户创建、认证和注销功能。
用户资料管理：允许用户更新个人信息，包括昵称、头像等。
第三方登录：通过集成OAuth2认证，支持社交媒体等第三方平台登录，确保用户数据加密存储，并明确隐私政策。

- 聊天功能
实时消息发送和接收：利用WebSocket实现高效的实时通信。
支持多种消息类型：支持文本、表情、图片、文件等多种消息类型的发送和接收。
消息状态管理：引入“已读”状态同步机制，确保消息状态在所有设备上保持一致。

- 聊天室管理
创建和加入聊天室：用户可以创建新的聊天室或加入现有聊天室。
聊天室元数据：增加聊天室的最大成员数、公开/私有标志等属性，以及聊天室的主题和描述。
聊天室成员管理：定义清晰的角色（管理员、普通成员等），并确定相应的权限（踢人、禁言等）。

- 历史记录
数据保留策略：根据法律法规制定聊天记录的保存与删除策略，考虑是否允许用户手动删除记录。
保存和恢复聊天记录：保存聊天记录以支持检索，并允许用户在需要时恢复历史聊天记录。

- 社群功能
创建社群：允许用户根据不同主题创建社群，并进行社群成员管理。

- 文件共享
安全性措施：对上传文件进行类型检查和病毒扫描，以防止恶意文件上传。
存储方案：使用云存储（如MinIO）来处理文件的上传和下载，支持文件预览和分享链接。

- 通知与提醒
个性化设置：允许用户自定义通知频率和方式，避免通知疲劳。
提醒用户新消息或活动：及时提醒用户关于新消息或社群活动。
系统通知：管理员可以通过系统通知发布公告等信息。

- 搜索功能
高效索引：使用Elasticsearch等工具对聊天记录进行高效索引，以提高搜索性能。
搜索聊天记录和用户：允许用户按关键词检索消息和搜索用户。

- 聊天机器人
智能化设计：集成AI聊天机器人，确保其响应时间短，并遵循隐私保护原则，以提供自动回复功能。


=================

1. 用户管理模块
功能:
用户注册、登录、登出
用户资料管理（昵称、头像等）
第三方登录集成（OAuth2）
接口:
用户创建、认证、注销
更新用户信息
第三方登录处理
2. 聊天功能模块
功能:
实时消息发送和接收（WebSocket）
支持多种消息类型（文本、表情、图片、文件等）
消息状态管理（已读/未读状态）
接口:
消息发送与接收
消息状态更新
3. 聊天室管理模块
功能:
创建和加入聊天室
聊天室元数据管理（最大成员数、公开/私有标志等）
聊天室成员管理（角色定义、权限控制）
接口:
聊天室创建与加入
聊天室信息获取
成员管理操作（踢人、禁言等）
4. 历史记录模块
功能:
数据保留策略制定
聊天记录保存与恢复
接口:
保存聊天记录
恢复历史记录
5. 社群功能模块
功能:
创建社群及社群成员管理
接口:
社群创建与信息获取
加入与离开社群
6. 文件共享模块
功能:
文件上传、下载与预览
安全性措施（类型检查、病毒扫描）
接口:
上传文件
获取文件信息
下载文件
删除文件
7. 通知与提醒模块
功能:
个性化通知设置
新消息或活动提醒
系统通知发布
接口:
设置通知偏好
发布系统通知
8. 搜索功能模块
功能:
聊天记录高效索引与检索
接口:
按关键词搜索聊天记录
搜索用户信息
9. 聊天机器人模块
功能:
集成AI聊天机器人，提供自动回复功能
接口:
接收并处理用户消息
返回机器人的响应

===================


router/user.py

1. 用户注册
POST /users/register
请求体: 包含用户名、密码、邮箱等信息。
功能: 创建新用户，并返回用户信息。
2. 用户登录
POST /users/login
请求体: 包含用户名/邮箱和密码。
功能: 验证用户身份并返回JWT令牌或会话信息。
3. 用户登出
POST /users/logout
功能: 注销当前用户的会话（如果使用JWT，可以选择不做任何操作）。
4. 获取当前用户信息
GET /users/me
功能: 返回当前登录用户的信息（需要身份验证）。
5. 更新用户资料
PUT /users/me
请求体: 包含要更新的字段（如昵称、头像等）。
功能: 更新当前用户的信息。
6. 修改密码
PUT /users/me/password
请求体: 包含旧密码和新密码。
功能: 更新用户密码。
7. 删除用户账户
DELETE /users/me
功能: 删除当前用户的账户。
8. 第三方登录
GET /users/oauth/{provider}

路由参数: provider（如 Google, Facebook 等）。
功能: 重定向到第三方OAuth认证页面。
GET /users/oauth/callback

功能: 处理第三方OAuth回调并创建/返回用户信息。



==============

1. 创建聊天室
POST /rooms
请求体: 包含聊天室名称、最大成员数、公开/私有标志等信息。
功能: 创建新的聊天室，并返回聊天室信息。
2. 获取聊天室列表
GET /rooms
查询参数: 可选的过滤条件（如公开/私有）。
功能: 返回用户可以访问的聊天室列表。
3. 加入聊天室
POST /rooms/{room_id}/join
路由参数: room_id（聊天室 ID）。
功能: 用户加入指定的聊天室。
4. 离开聊天室
POST /rooms/{room_id}/leave
路由参数: room_id（聊天室 ID）。
功能: 用户离开指定的聊天室。
5. 获取聊天室信息
GET /rooms/{room_id}
路由参数: room_id（聊天室 ID）。
功能: 返回指定聊天室的信息，包括成员列表。
6. 更新聊天室信息
PUT /rooms/{room_id}
路由参数: room_id（聊天室 ID）。
请求体: 包含要更新的字段（如主题、描述等）。
功能: 更新指定聊天室的信息。
7. 删除聊天室
DELETE /rooms/{room_id}
路由参数: room_id（聊天室 ID）。
功能: 删除指定的聊天室（只有管理员可以执行）。
8. 聊天室成员管理
POST /rooms/{room_id}/members/{user_id}/kick

路由参数: room_id（聊天室 ID），user_id（用户 ID）。
功能: 管理员踢出指定用户。
POST /rooms/{room_id}/members/{user_id}/mute

路由参数: room_id（聊天室 ID），user_id（用户 ID）。
功能: 管理员禁言指定用户。
示例代码



====================

1. 上传文件
POST /files/upload
请求体: 包含文件数据。
功能: 用户上传文件，并返回文件的元数据（如文件ID、URL等）。
2. 获取文件信息
GET /files/{file_id}
路由参数: file_id（文件 ID）。
功能: 返回指定文件的详细信息，如文件名、大小、类型、上传时间等。
3. 下载文件
GET /files/download/{file_id}
路由参数: file_id（文件 ID）。
功能: 提供下载指定文件的链接。
4. 删除文件
DELETE /files/{file_id}
路由参数: file_id（文件 ID）。
功能: 删除指定文件，仅限于文件拥有者或管理员。
5. 列出用户上传的文件
GET /users/{user_id}/files
路由参数: user_id（用户 ID）。
查询参数: 可选的过滤条件（如文件类型、上传日期等）。
功能: 返回指定用户上传的所有文件列表。



==========================

1. 创建社群
POST /communities
请求体: 包含社群名称、描述、最大成员数等信息。
功能: 用户创建新的社群。
2. 获取社群信息
GET /communities/{community_id}
路由参数: community_id（社群 ID）。
功能: 返回指定社群的详细信息，包括成员列表和社群元数据。
3. 加入社群
POST /communities/{community_id}/join
路由参数: community_id（社群 ID）。
功能: 用户加入指定社群。
4. 离开社群
POST /communities/{community_id}/leave
路由参数: community_id（社群 ID）。
功能: 用户离开指定社群。
5. 列出用户所在的社群
GET /users/{user_id}/communities
路由参数: user_id（用户 ID）。
功能: 返回用户加入的所有社群列表。
6. 社群成员管理
POST /communities/{community_id}/members/{user_id}/role
路由参数: community_id（社群 ID），user_id（用户 ID）。
请求体: 包含新角色信息。
功能: 更新某个成员在社群中的角色（如管理员、普通成员）。

=====================


为了实现 history.py 模块，聊天记录的数据库设计需要考虑以下几个方面：数据结构、存储效率、检索性能等。根据需求，可以选择使用关系型数据库（如 MySQL）和非关系型数据库（如 MongoDB），同时引入 Elasticsearch 以增强搜索能力。

数据库设计
1. 关系型数据库设计（例如 MySQL）
表名: chat_messages

列名	类型	描述
id	INT (主键)	消息唯一标识
chat_room_id	VARCHAR	聊天室ID
user_id	VARCHAR	用户ID
content	TEXT	消息内容
timestamp	DATETIME	消息发送时间
索引:

在 chat_room_id 和 timestamp 上建立索引，以加快按聊天室和时间范围查询消息的速度。
2. 非关系型数据库设计（例如 MongoDB）
集合名: chat_history

{
    "_id": ObjectId,
    "chat_room_id": "string",
    "messages": [
        {
            "user_id": "string",
            "content": "string",
            "timestamp": "ISODate"
        }
    ]
}
这种设计允许将同一聊天室的所有消息存储在一个文档中，便于整体检索。

引入 Elasticsearch 的理由
如果系统需要高效的文本搜索功能，尤其是支持关键词搜索、模糊匹配或复杂查询，则可以引入 Elasticsearch。它适合处理大量数据并提供快速的搜索能力。

使用场景：
全文搜索: 支持对聊天记录中的关键字进行快速检索。
聚合分析: 可以对消息进行统计分析，例如用户活跃度、话题热度等。
实时更新: 当新消息到达时，可以实时更新索引，提高搜索的及时性。
整体架构建议
MySQL/MongoDB: 存储聊天记录的基本信息，包括用户、内容和时间戳。选择MongoDB时，可利用其灵活的数据模型。

Elasticsearch: 用于增强搜索能力，特别是在需要快速响应的情况下，比如用户输入关键词时。

数据同步: 如果使用了Elasticsearch，需要设计机制将新的聊天记录从MySQL/MongoDB同步到Elasticsearch。这可以通过定期批量同步或者触发事件来实现。

总结
使用关系型数据库或非关系型数据库都可以满足基本的聊天记录存储需求。
引入Elasticsearch可以显著提升搜索性能，特别是在需要复杂查询和大规模数据检索的场景下。
具体选择取决于应用的规模、预期的负载以及开发团队的技术栈熟悉程度。