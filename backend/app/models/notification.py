"""通知模型。"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from app import db


class Notification(db.Model):
    """通知模型。"""
    __tablename__ = 'notifications'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    related_id = Column(UUID(as_uuid=True))
    related_type = Column(String(50))
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    user = db.relationship('Profile', back_populates='notifications')

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'related_id': str(self.related_id) if self.related_id else None,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }
