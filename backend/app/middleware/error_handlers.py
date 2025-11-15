"""全局错误处理器。"""
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    """注册错误处理器。"""
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({'message': e.description}), e.code
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f'Unhandled exception: {str(e)}')
        return jsonify({'message': '服务器内部错误'}), 500
