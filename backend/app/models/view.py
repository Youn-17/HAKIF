"""视图模型。"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from app import db


class View(db.Model):
    """课程视图模型。"""
    __tablename__ = 'views'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False)
    is_main_view = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship('Course', back_populates='views')
    creator = db.relationship('Profile')
    notes = db.relationship('Note', back_populates='view', lazy='dynamic')

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'course_id': str(self.course_id),
            'name': self.name,
            'description': self.description,
            'created_by': str(self.created_by),
            'is_main_view': self.is_main_view,
            'note_count': self.notes.count(),
            'created_at': self.created_at.isoformat(),
        }
