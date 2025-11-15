"""管理员API端点。"""
from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Profile, TeacherApplication
from datetime import datetime

ns = Namespace('admin', description='管理员功能')

@ns.route('/teacher-applications')
class TeacherApplicationList(Resource):
    @jwt_required()
    def get(self):
        """获取待审核教师列表"""
        user_id = get_jwt_identity()
        user = Profile.query.get(user_id)
        
        if user.role != 'admin':
            return {'message': '需要管理员权限'}, 403
        
        applications = TeacherApplication.query.filter_by(
            status='pending'
        ).all()
        
        return {
            'applications': [a.to_dict() for a in applications]
        }, 200

@ns.route('/teacher-applications/<string:app_id>/review')
class ReviewTeacherApplication(Resource):
    @jwt_required()
    def put(self, app_id):
        """审核教师申请"""
        user_id = get_jwt_identity()
        user = Profile.query.get(user_id)
        
        if user.role != 'admin':
            return {'message': '需要管理员权限'}, 403
        
        data = request.get_json()
        action = data.get('action')  # approved/rejected
        
        application = TeacherApplication.query.get(app_id)
        if not application:
            return {'message': '申请不存在'}, 404
        
        application.status = action
        application.reviewed_by = user_id
        application.reviewed_at = datetime.utcnow()
        application.review_comment = data.get('comment')
        
        if action == 'approved':
            # 更新申请人角色为教师
            applicant = Profile.query.get(application.applicant_id)
            applicant.role = 'teacher'
        
        db.session.commit()
        
        return {'message': f'申请已{action}'}, 200
