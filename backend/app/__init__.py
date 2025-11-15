"""
Flask应用工厂。

使用应用工厂模式创建Flask应用实例。
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from typing import Optional

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


def create_app(config_name: Optional[str] = None) -> Flask:
    """应用工厂函数。

    Args:
        config_name: 配置名称 (development/testing/production)

    Returns:
        配置好的Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    from config import get_config
    app.config.from_object(get_config(config_name))

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    # 配置CORS
    CORS(
        app,
        origins=app.config['CORS_ORIGINS'],
        supports_credentials=True
    )

    # 注册蓝图
    from app.api import register_blueprints
    register_blueprints(app)

    # 注册错误处理器
    from app.middleware.error_handlers import register_error_handlers
    register_error_handlers(app)

    # 注册钩子函数
    from app.middleware.hooks import register_hooks
    register_hooks(app)

    # 创建上传目录
    import os
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)

    # 创建日志目录
    log_file = app.config.get('LOG_FILE')
    if log_file:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    # 配置日志
    from app.utils.logger import setup_logging
    setup_logging(app)

    return app
