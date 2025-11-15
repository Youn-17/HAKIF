"""日志配置。"""
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask


def setup_logging(app: Flask) -> None:
    """配置应用日志。"""
    if app.config.get('LOG_FILE'):
        handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=app.config.get('LOG_MAX_BYTES', 10485760),
            backupCount=app.config.get('LOG_BACKUP_COUNT', 30)
        )
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        app.logger.addHandler(handler)
        app.logger.setLevel(
            getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
        )
