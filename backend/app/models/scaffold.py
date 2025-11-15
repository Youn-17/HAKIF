"""脚手架模型。"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from app import db


class Scaffold(db.Model):
    """脚手架模型。"""
    __tablename__ = 'scaffolds'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    course = db.relationship('Course')
