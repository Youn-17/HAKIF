"""
应用配置文件。

包含开发、测试、生产环境的配置类。
严格遵循PEP8规范，行宽不超过79字符。
"""
import os
from datetime import timedelta
from typing import Optional


class Config:
    """基础配置类。"""

    # 应用基础配置
    SECRET_KEY: str = os.getenv(
        'SECRET_KEY',
        'dev-secret-key-change-in-production'
    )

    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/hakif'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # JWT配置
    JWT_SECRET_KEY: str = os.getenv(
        'JWT_SECRET_KEY',
        'jwt-secret-key-change-in-production'
    )
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)

    # CORS配置
    CORS_ORIGINS: list = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]

    # 文件上传配置
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_FOLDER: str = os.path.join(
        os.path.dirname(__file__),
        'uploads'
    )
    ALLOWED_EXTENSIONS: set = {
        'png', 'jpg', 'jpeg', 'gif', 'webp',
        'pdf', 'doc', 'docx', 'txt', 'md'
    }

    # AI服务配置
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    DEEPSEEK_API_KEY: Optional[str] = os.getenv('DEEPSEEK_API_KEY')
    AI_SERVICE_URL: str = os.getenv(
        'AI_SERVICE_URL',
        'http://localhost:8000'
    )

    # Redis配置
    REDIS_URL: str = os.getenv(
        'REDIS_URL',
        'redis://localhost:6379/0'
    )

    # Celery配置
    CELERY_BROKER_URL: str = os.getenv(
        'CELERY_BROKER_URL',
        'redis://localhost:6379/0'
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        'CELERY_RESULT_BACKEND',
        'redis://localhost:6379/0'
    )

    # 日志配置
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = 'logs/app.log'
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 30

    # 速率限制
    RATELIMIT_ENABLED: bool = True
    RATELIMIT_STORAGE_URL: str = os.getenv(
        'REDIS_URL',
        'redis://localhost:6379/0'
    )


class DevelopmentConfig(Config):
    """开发环境配置。"""

    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True
    TESTING: bool = False


class TestingConfig(Config):
    """测试环境配置。"""

    DEBUG: bool = False
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'TEST_DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/hakif_test'
    )
    # 禁用CSRF保护以便测试
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(Config):
    """生产环境配置。"""

    DEBUG: bool = False
    TESTING: bool = False

    # 生产环境必须使用环境变量
    @property
    def SECRET_KEY(self) -> str:
        """确保生产环境有密钥。"""
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise ValueError(
                'SECRET_KEY must be set in production'
            )
        return secret_key

    @property
    def JWT_SECRET_KEY(self) -> str:
        """确保生产环境有JWT密钥。"""
        jwt_key = os.getenv('JWT_SECRET_KEY')
        if not jwt_key:
            raise ValueError(
                'JWT_SECRET_KEY must be set in production'
            )
        return jwt_key


# 配置字典
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: Optional[str] = None) -> Config:
    """获取配置对象。

    Args:
        config_name: 配置名称，如果为None则从环境变量读取

    Returns:
        配置对象实例
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    return config_by_name.get(config_name, DevelopmentConfig)()
