"""AI交互模型。"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from app import db


class AIInteraction(db.Model):
    """AI交互记录模型。"""
    __tablename__ = 'ai_interactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id'), index=True)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id'), index=True)
    prompt_type = Column(String(50), nullable=False)
    ai_response = Column(JSONB, nullable=False)
    user_accepted = Column(Boolean)
    is_ignored = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)

    user = db.relationship('Profile')
    note = db.relationship('Note')
