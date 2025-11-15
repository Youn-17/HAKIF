"""
数据库模型包。

包含所有SQLAlchemy模型定义。
"""
from app.models.user import Profile, TeacherApplication
from app.models.course import Course, CourseMember
from app.models.note import Note, NoteVersion, NoteInteraction
from app.models.view import View
from app.models.group import Group, GroupMember
from app.models.scaffold import Scaffold
from app.models.ai_interaction import AIInteraction
from app.models.notification import Notification

__all__ = [
    'Profile',
    'TeacherApplication',
    'Course',
    'CourseMember',
    'Note',
    'NoteVersion',
    'NoteInteraction',
    'View',
    'Group',
    'GroupMember',
    'Scaffold',
    'AIInteraction',
    'Notification',
]
