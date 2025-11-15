"""数据验证工具。"""
import re


def validate_email(email: str) -> bool:
    """验证邮箱格式。"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
