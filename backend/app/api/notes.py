"""笔记API端点。"""
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Note, Profile

ns = Namespace('notes', description='笔记管理')

@ns.route('/')
class NoteList(Resource):
    @jwt_required()
    def get(self):
        """获取笔记列表"""
        course_id = request.args.get('course_id')
        if not course_id:
            return {'message': '需要提供course_id'}, 400
        
        notes = Note.query.filter_by(course_id=course_id).all()
        return {'notes': [n.to_dict() for n in notes]}, 200
    
    @jwt_required()
    def post(self):
        """创建笔记"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        note = Note(
            title=data['title'],
            content=data['content'],
            author_id=user_id,
            course_id=data['course_id'],
            view_id=data.get('view_id'),
            note_type=data.get('note_type', 'standard'),
            parent_note_id=data.get('parent_note_id'),
            tags=data.get('tags', [])
        )
        db.session.add(note)
        db.session.commit()

        return note.to_dict(), 201

@ns.route('/<string:note_id>')
class NoteDetail(Resource):
    @jwt_required()
    def get(self, note_id):
        """获取单个笔记"""
        note = Note.query.get(note_id)
        if not note:
            return {'message': '笔记不存在'}, 404

        return note.to_dict(), 200

    @jwt_required()
    def put(self, note_id):
        """更新笔记"""
        user_id = get_jwt_identity()
        note = Note.query.get(note_id)

        if not note:
            return {'message': '笔记不存在'}, 404

        if note.author_id != user_id:
            return {'message': '无权修改此笔记'}, 403

        data = request.get_json()
        if 'title' in data:
            note.title = data['title']
        if 'content' in data:
            note.content = data['content']
        if 'tags' in data:
            note.tags = data['tags']

        db.session.commit()
        return note.to_dict(), 200

    @jwt_required()
    def delete(self, note_id):
        """删除笔记"""
        user_id = get_jwt_identity()
        note = Note.query.get(note_id)

        if not note:
            return {'message': '笔记不存在'}, 404

        if note.author_id != user_id:
            return {'message': '无权删除此笔记'}, 403

        db.session.delete(note)
        db.session.commit()
        return {'message': '删除成功'}, 200
