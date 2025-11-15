# Human-AI Knowledge Interaction Forum

一个创新的在线协作学习平台，通过课程化的知识建构空间，结合AI智能助手提供个性化学习支持。

## 技术架构

### 混合架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    用户界面层                            │
│            Next.js 14 + TypeScript + React              │
│            Tailwind CSS + shadcn/ui                     │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────┴────────────────────────────────────┐
│                   业务逻辑层                             │
│              Python Flask 3.0+                          │
│           JWT认证 + 权限控制                            │
└────────────┬───────────────────┬────────────────────────┘
             │                   │
    ┌────────┴────────┐    ┌────┴─────────────────┐
    │   核心API服务    │    │   AI分析服务         │
    │   Flask         │    │   FastAPI           │
    │   (Port 5000)   │    │   Claude API        │
    └────────┬────────┘    │   (Port 8000)       │
             │             └──────────────────────┘
    ┌────────┴────────┐
    │   数据访问层     │
    │   SQLAlchemy    │
    │   PostgreSQL    │
    └─────────────────┘
```

## 技术栈

### 后端 (Python 3.12+)
- **Web框架**: Flask 3.0+
- **AI服务**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: PostgreSQL 15+
- **认证**: Flask-JWT-Extended
- **测试**: pytest + pytest-cov

### 前端 (TypeScript)
- **框架**: Next.js 14
- **UI库**: shadcn/ui + Tailwind CSS
- **富文本**: TipTap 2
- **可视化**: React Flow

## 快速开始

### 启动后端
```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### 启动前端
```bash
cd frontend
npm install
npm run dev
```

访问：http://localhost:3000
