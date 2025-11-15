"""
用户相关数据模型。

包含Profile(用户资料)和TeacherApplication(教师申请)模型。
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import (
    Column, String, Boolean, DateTime,
    Enum as SQLEnum, Text, ForeignKey, CheckConstraint
)
from app import db
import bcrypt


class Profile(db.Model):
    """用户资料模型。"""

    __tablename__ = 'profiles'

    # 主键
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # 基本信息
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    chinese_name = Column(String(100), nullable=False, index=True)
    pinyin_first_name = Column(String(100), nullable=False)
    pinyin_family_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    gender = Column(
        SQLEnum('男', '女', '其他', name='gender_enum'),
        nullable=False
    )
    school = Column(String(255), nullable=False, index=True)
    major = Column(String(255), nullable=False)

    # 角色
    role = Column(
        SQLEnum('student', 'teacher', 'admin', name='role_enum'),
        nullable=False,
        default='student',
        index=True
    )

    # 额外信息
    avatar_url = Column(Text)
    additional_info = Column(JSONB, default={})

    # 时间戳
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # 关系
    courses_created = db.relationship(
        'Course',
        back_populates='creator',
        lazy='dynamic'
    )
    course_memberships = db.relationship(
        'CourseMember',
        back_populates='user',
        lazy='dynamic'
    )
    notes = db.relationship(
        'Note',
        back_populates='author',
        lazy='dynamic'
    )
    notifications = db.relationship(
        'Notification',
        back_populates='user',
        lazy='dynamic'
    )

    def set_password(self, password: str) -> None:
        """设置密码哈希。

        Args:
            password: 明文密码
        """
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """验证密码。

        Args:
            password: 待验证的明文密码

        Returns:
            密码是否正确
        """
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """转换为字典。

        Args:
            include_sensitive: 是否包含敏感信息

        Returns:
            用户资料字典
        """
        data = {
            'id': str(self.id),
            'email': self.email,
            'chinese_name': self.chinese_name,
            'pinyin_first_name': self.pinyin_first_name,
            'pinyin_family_name': self.pinyin_family_name,
            'phone': self.phone if include_sensitive else None,
            'gender': self.gender,
            'school': self.school,
            'major': self.major,
            'role': self.role,
            'avatar_url': self.avatar_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

        if include_sensitive:
            data['additional_info'] = self.additional_info

        return data

    def __repr__(self) -> str:
        """字符串表示。"""
        return f'<Profile {self.chinese_name} ({self.email})>'


class TeacherApplication(db.Model):
    """教师申请模型。"""

    __tablename__ = 'teacher_applications'

    # 主键
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # 申请人
    applicant_id = Column(
        UUID(as_uuid=True),
        ForeignKey('profiles.id', ondelete='CASCADE'),
        nullable=False
    )

    # 申请信息
    application_info = Column(JSONB, nullable=False)

    # 审核状态
    status = Column(
        SQLEnum(
            'pending',
            'approved',
            'rejected',
            name='application_status_enum'
        ),
        default='pending',
        nullable=False,
        index=True
    )

    # 审核信息
    reviewed_by = Column(
        UUID(as_uuid=True),
        ForeignKey('profiles.id')
    )
    review_comment = Column(Text)

    # 时间戳
    applied_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    reviewed_at = Column(DateTime(timezone=True))

    # 关系
    applicant = db.relationship(
        'Profile',
        foreign_keys=[applicant_id],
        backref='teacher_applications'
    )
    reviewer = db.relationship(
        'Profile',
        foreign_keys=[reviewed_by]
    )

    # 约束
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name='check_application_status'
        ),
    )

    def to_dict(self) -> dict:
        """转换为字典。

        Returns:
            申请信息字典
        """
        return {
            'id': str(self.id),
            'applicant_id': str(self.applicant_id),
            'applicant': self.applicant.to_dict() if self.applicant else None,
            'application_info': self.application_info,
            'status': self.status,
            'review_comment': self.review_comment,
            'reviewed_by': (
                str(self.reviewed_by) if self.reviewed_by else None
            ),
            'applied_at': self.applied_at.isoformat(),
            'reviewed_at': (
                self.reviewed_at.isoformat()
                if self.reviewed_at else None
            ),
        }

    def __repr__(self) -> str:
        """字符串表示。"""
        return (
            f'<TeacherApplication {self.id} '
            f'status={self.status}>'
        )
