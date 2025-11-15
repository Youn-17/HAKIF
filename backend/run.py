"""Flask应用启动入口。

运行命令：python run.py
"""
import os
from app import create_app, db


# 创建应用实例
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.cli.command()
def init_db():
    """初始化数据库。"""
    db.create_all()
    print('数据库初始化完成')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
