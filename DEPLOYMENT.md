# 部署指南

## 系统要求

- Python 3.12+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (推荐)

## 快速开始 (Docker方式)

### 1. 克隆项目
```bash
git clone <repository-url>
cd HAKIF
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填写必要的配置
```

必须配置的环境变量：
- `ANTHROPIC_API_KEY`: Claude API密钥
- `DATABASE_URL`: PostgreSQL连接字符串
- `SECRET_KEY`: Flask密钥
- `JWT_SECRET_KEY`: JWT密钥

### 3. 启动所有服务
```bash
docker-compose up -d
```

服务端口：
- 前端：http://localhost:3000
- 后端API：http://localhost:5000
- AI服务：http://localhost:8000
- PostgreSQL：localhost:5432
- Redis：localhost:6379

### 4. 初始化数据库
```bash
docker-compose exec backend flask db upgrade
```

### 5. 创建管理员账号
```bash
docker-compose exec backend python -c "
from app import create_app, db
from app.models import Profile

app = create_app()
with app.app_context():
    admin = Profile(
        email='admin@example.com',
        chinese_name='系统管理员',
        pinyin_first_name='Admin',
        pinyin_family_name='System',
        phone='13800000000',
        gender='其他',
        school='系统',
        major='管理',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print('管理员账号创建成功')
"
```

## 本地开发模式

### 后端开发

```bash
cd backend

# 创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 启动Flask服务
python run.py
```

后端API文档：http://localhost:5000/api/docs

### AI服务开发

```bash
cd backend/ai_service

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload --port 8000
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端访问：http://localhost:3000

## 代码规范检查

### Python代码检查
```bash
cd backend

# Black格式化
black . --line-length 79

# Flake8检查
flake8 app/ --max-line-length=79

# MyPy类型检查
mypy app/
```

### TypeScript代码检查
```bash
cd frontend

# ESLint检查
npm run lint

# 类型检查
npm run type-check
```

## 测试

### 后端测试
```bash
cd backend

# 运行所有测试
pytest

# 测试覆盖率报告
pytest --cov=app --cov-report=html

# 查看报告
open htmlcov/index.html
```

### 前端测试
```bash
cd frontend

# 运行测试
npm test

# E2E测试
npm run test:e2e
```

## 生产环境部署

### 1. 构建生产镜像
```bash
docker-compose -f docker-compose.prod.yml build
```

### 2. 启动生产服务
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 3. 配置Nginx反向代理
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 后端API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 数据库备份

### 备份
```bash
docker-compose exec db pg_dump -U postgres hakif > backup_$(date +%Y%m%d).sql
```

### 恢复
```bash
docker-compose exec -T db psql -U postgres hakif < backup_20250115.sql
```

## 常见问题

### 数据库连接失败
检查PostgreSQL是否启动：
```bash
docker-compose ps
docker-compose logs db
```

### AI服务调用失败
检查环境变量：
```bash
echo $ANTHROPIC_API_KEY
```

### 前端无法连接后端
检查CORS配置和API_URL环境变量。

## 性能优化建议

1. **数据库索引优化**：定期分析慢查询
2. **Redis缓存**：缓存频繁查询的数据
3. **CDN加速**：静态资源使用CDN
4. **负载均衡**：多实例部署

## 监控和日志

- 后端日志：`backend/logs/app.log`
- 访问Sentry查看错误追踪
- 使用Prometheus监控系统指标

## 安全检查清单

- [ ] 更改默认密钥
- [ ] 配置HTTPS
- [ ] 启用防火墙
- [ ] 定期更新依赖
- [ ] 配置数据库访问控制
- [ ] 启用请求速率限制
- [ ] 配置备份策略
