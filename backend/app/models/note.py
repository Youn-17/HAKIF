"""笔记相关数据模型。"""
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey,  Enum as SQLEnum
from app import db


class Note(db.Model):
    """笔记模型。"""
    __tablename__ = 'notes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(JSONB, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id', ondelete='CASCADE'), nullable=False, index=True)
    view_id = Column(UUID(as_uuid=True), ForeignKey('views.id'))
    scaffold_id = Column(UUID(as_uuid=True), ForeignKey('scaffolds.id'))
    note_type = Column(SQLEnum('standard', 'response', 'synthesis', name='note_type_enum'), nullable=False, default='standard')
    parent_note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id'))
    tags = Column(ARRAY(Text))
    version_number = Column(Integer, default=1)
    is_group_note = Column(db.Boolean, default=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('groups.id'))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    author = db.relationship('Profile', back_populates='notes')
    course = db.relationship('Course', back_populates='notes')
    view = db.relationship('View', back_populates='notes')
    versions = db.relationship('NoteVersion', back_populates='note', lazy='dynamic')

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'content': self.content,
            'author_id': str(self.author_id),
            'author': self.author.to_dict() if self.author else None,
            'course_id': str(self.course_id),
            'view_id': str(self.view_id) if self.view_id else None,
            'note_type': self.note_type,
            'parent_note_id': str(self.parent_note_id) if self.parent_note_id else None,
            'tags': self.tags,
            'version_number': self.version_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class NoteVersion(db.Model):
    """笔记版本模型。"""
    __tablename__ = 'note_versions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(JSONB, nullable=False)
    version_number = Column(Integer, nullable=False)
    change_description = Column(Text)
    edited_by = Column(UUID(as_uuid=True), ForeignKey('profiles.id'))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    note = db.relationship('Note', back_populates='versions')
    editor = db.relationship('Profile')


class NoteInteraction(db.Model):
    """笔记互动模型。"""
    __tablename__ = 'note_interactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    note_id = Column(UUID(as_uuid=True), ForeignKey('notes.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('profiles.id'), nullable=False, index=True)
    interaction_type = Column(String(50), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
