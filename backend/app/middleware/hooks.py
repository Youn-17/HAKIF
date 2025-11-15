"""请求钩子。"""
from flask import Flask


def register_hooks(app: Flask) -> None:
    """注册请求钩子。"""
    
    @app.after_request
    def after_request(response):
        response.headers.add('X-Content-Type-Options', 'nosniff')
        response.headers.add('X-Frame-Options', 'SAMEORIGIN')
        response.headers.add('X-XSS-Protection', '1; mode=block')
        return response
