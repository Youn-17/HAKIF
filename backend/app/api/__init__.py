"""API蓝图注册。"""
from flask import Flask, Blueprint
from flask_restx import Api

# 创建API实例
api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    api_bp,
    version='1.0',
    title='Human-AI Knowledge Interaction Forum API',
    description='知识交互论坛API文档',
    doc='/docs'
)


def register_blueprints(app: Flask) -> None:
    """注册所有蓝图。
    
    Args:
        app: Flask应用实例
    """
    # 导入命名空间
    from app.api.auth import ns as auth_ns
    from app.api.courses import ns as courses_ns
    from app.api.notes import ns as notes_ns
    from app.api.admin import ns as admin_ns
    
    # 注册命名空间
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(courses_ns, path='/courses')
    api.add_namespace(notes_ns, path='/notes')
    api.add_namespace(admin_ns, path='/admin')
    
    # 注册蓝图
    app.register_blueprint(api_bp)
