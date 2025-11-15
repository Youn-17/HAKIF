"""分组模型。"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum, UniqueConstraint
from app import db


class Group(db.Model):
    """课程分组模型。"""
    __tablename__ = 'groups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    group_type = Column(SQLEnum('open', 'closed', 'assigned', name='group_type_enum'), nullable=False)
    max_members = Column(Integer, default=10)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    course = db.relationship('Course', back_populates='groups')
    creator = db.relationship('Profile')
    members = db.relationship('GroupMember', back_populates='group', lazy='dynamic')


class GroupMember(db.Model):
    """分组成员模型。"""
    __tablename__ = 'group_members'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id', ondelete='CASCADE'), nullable=False, index=True)
    profile_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    role = Column(SQLEnum('leader', 'member', name='group_role_enum'), default='member')
    joined_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    group = db.relationship('Group', back_populates='members')
    user = db.relationship('Profile')

    __table_args__ = (UniqueConstraint('group_id', 'profile_id'),)
