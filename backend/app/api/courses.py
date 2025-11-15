"""课程API端点。"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Course, CourseMember, Profile

ns = Namespace('courses', description='课程管理')

course_model = ns.model('Course', {
    'name': fields.String(required=True, description='课程名称'),
    'description': fields.String(description='课程描述'),
    'access_code': fields.String(required=True, description='访问代码'),
})

@ns.route('/')
class CourseList(Resource):
    @jwt_required()
    def get(self):
        """获取课程列表"""
        user_id = get_jwt_identity()
        user = Profile.query.get(user_id)
        
        if user.role == 'student':
            # 学生看到所有课程
            courses = Course.query.filter_by(is_active=True).all()
        else:
            # 教师看到自己创建的课程
            courses = Course.query.filter_by(created_by=user_id).all()
        
        return {'courses': [c.to_dict() for c in courses]}, 200
    
    @jwt_required()
    @ns.expect(course_model)
    def post(self):
        """创建课程（教师）"""
        user_id = get_jwt_identity()
        user = Profile.query.get(user_id)
        
        if user.role != 'teacher':
            return {'message': '只有教师可以创建课程'}, 403
        
        data = request.get_json()
        course = Course(
            name=data['name'],
            description=data.get('description'),
            access_code=data['access_code'],
            created_by=user_id
        )
        db.session.add(course)
        db.session.commit()
        
        return course.to_dict(), 201

@ns.route('/<string:course_id>')
class CourseDetail(Resource):
    @jwt_required()
    def get(self, course_id):
        """获取单个课程详情"""
        course = Course.query.get(course_id)
        if not course:
            return {'message': '课程不存在'}, 404

        return course.to_dict(), 200

@ns.route('/<string:course_id>/join')
class JoinCourse(Resource):
    @jwt_required()
    def post(self, course_id):
        """加入课程"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        course = Course.query.get(course_id)
        if not course:
            return {'message': '课程不存在'}, 404
        
        if course.access_code != data.get('access_code'):
            return {'message': '访问代码错误'}, 400
        
        # 检查是否已加入
        existing = CourseMember.query.filter_by(
            course_id=course_id,
            user_id=user_id
        ).first()
        if existing:
            return {'message': '已加入该课程'}, 400
        
        member = CourseMember(course_id=course_id, user_id=user_id)
        db.session.add(member)
        db.session.commit()
        
        return {'message': '成功加入课程'}, 200
