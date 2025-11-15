"""
课程相关数据模型。

包含Course(课程)和CourseMember(课程成员)模型。
"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column, String, Text, Boolean, DateTime,
    Integer, ForeignKey, UniqueConstraint, Enum as SQLEnum
)
from app import db


class Course(db.Model):
    """课程模型。"""

    __tablename__ = 'courses'

    # 主键
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # 课程信息
    name = Column(String(255), nullable=False)
    description = Column(Text)
    access_code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    # 创建者
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey('profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # 状态
    is_active = Column(Boolean, default=True, nullable=False)
    status = Column(
        SQLEnum(
            'active',
            'archived',
            'deleted',
            name='course_status_enum'
        ),
        default='active',
        nullable=False
    )

    # 学期信息
    semester_start = Column(DateTime(timezone=True))
    semester_end = Column(DateTime(timezone=True))

    # 成员限制
    max_members = Column(Integer, default=50)

    # 时间戳
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # 关系
    creator = db.relationship(
        'Profile',
        back_populates='courses_created'
    )
    members = db.relationship(
        'CourseMember',
        back_populates='course',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    notes = db.relationship(
        'Note',
        back_populates='course',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    views = db.relationship(
        'View',
        back_populates='course',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    groups = db.relationship(
        'Group',
        back_populates='course',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def to_dict(self, include_members: bool = False) -> dict:
        """转换为字典。

        Args:
            include_members: 是否包含成员信息

        Returns:
            课程信息字典
        """
        data = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'access_code': self.access_code,
            'created_by': str(self.created_by),
            'creator': self.creator.to_dict() if self.creator else None,
            'is_active': self.is_active,
            'status': self.status,
            'semester_start': (
                self.semester_start.isoformat()
                if self.semester_start else None
            ),
            'semester_end': (
                self.semester_end.isoformat()
                if self.semester_end else None
            ),
            'max_members': self.max_members,
            'member_count': self.members.count(),
            'note_count': self.notes.count(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

        if include_members:
            data['members'] = [
                m.to_dict() for m in self.members.all()
            ]

        return data

    def __repr__(self) -> str:
        """字符串表示。"""
        return f'<Course {self.name} ({self.access_code})>'


class CourseMember(db.Model):
    """课程成员模型。"""

    __tablename__ = 'course_members'

    # 主键
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # 课程和用户
    course_id = Column(
        UUID(as_uuid=True),
        ForeignKey('courses.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    # 角色
    role = Column(
        SQLEnum('member', 'assistant', name='member_role_enum'),
        default='member',
        nullable=False
    )

    # 加入时间
    joined_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # 关系
    course = db.relationship('Course', back_populates='members')
    user = db.relationship('Profile', back_populates='course_memberships')

    # 唯一约束
    __table_args__ = (
        UniqueConstraint('course_id', 'user_id', name='uq_course_user'),
    )

    def to_dict(self) -> dict:
        """转换为字典。

        Returns:
            成员信息字典
        """
        return {
            'id': str(self.id),
            'course_id': str(self.course_id),
            'user_id': str(self.user_id),
            'user': self.user.to_dict() if self.user else None,
            'role': self.role,
            'joined_at': self.joined_at.isoformat(),
        }

    def __repr__(self) -> str:
        """字符串表示。"""
        return f'<CourseMember course={self.course_id} user={self.user_id}>'
