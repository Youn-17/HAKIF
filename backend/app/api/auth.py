"""认证API端点。"""
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app import db
from app.models import Profile
from app.utils.validators import validate_email

ns = Namespace('auth', description='用户认证')

# API模型定义
register_model = ns.model('Register', {
    'email': fields.String(required=True, description='邮箱'),
    'password': fields.String(required=True, description='密码'),
    'chinese_name': fields.String(required=True, description='中文姓名'),
    'pinyin_first_name': fields.String(required=True, description='拼音名'),
    'pinyin_family_name': fields.String(required=True, description='拼音姓'),
    'phone': fields.String(required=True, description='手机号'),
    'gender': fields.String(required=True, description='性别'),
    'school': fields.String(required=True, description='学校'),
    'major': fields.String(required=True, description='专业'),
    'role': fields.String(required=True, description='角色'),
})

login_model = ns.model('Login', {
    'email': fields.String(required=True, description='邮箱'),
    'password': fields.String(required=True, description='密码'),
})


@ns.route('/register')
class Register(Resource):
    """用户注册"""
    
    @ns.expect(register_model)
    @ns.doc('register_user')
    def post(self):
        """注册新用户"""
        data = request.get_json()
        
        # 验证必填字段
        required_fields = [
            'email', 'password', 'chinese_name',
            'pinyin_first_name', 'pinyin_family_name',
            'phone', 'gender', 'school', 'major', 'role'
        ]
        for field in required_fields:
            if not data.get(field):
                return {'message': f'缺少必填字段: {field}'}, 400
        
        # 验证邮箱格式
        if not validate_email(data['email']):
            return {'message': '邮箱格式不正确'}, 400
        
        # 检查邮箱是否已存在
        if Profile.query.filter_by(email=data['email']).first():
            return {'message': '该邮箱已被注册'}, 400
        
        # 创建用户
        user = Profile(
            email=data['email'],
            chinese_name=data['chinese_name'],
            pinyin_first_name=data['pinyin_first_name'],
            pinyin_family_name=data['pinyin_family_name'],
            phone=data['phone'],
            gender=data['gender'],
            school=data['school'],
            major=data['major'],
            role=data['role'],
            additional_info=data.get('additional_info', {})
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return {
            'message': '注册成功',
            'user': user.to_dict()
        }, 201


@ns.route('/login')
class Login(Resource):
    """用户登录"""
    
    @ns.expect(login_model)
    @ns.doc('login_user')
    def post(self):
        """用户登录"""
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'message': '邮箱和密码不能为空'}, 400
        
        user = Profile.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return {'message': '邮箱或密码错误'}, 401
        
        # 生成JWT令牌
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }, 200


@ns.route('/me')
class Me(Resource):
    """获取当前用户信息"""
    
    @jwt_required()
    @ns.doc('get_current_user', security='Bearer')
    def get(self):
        """获取当前登录用户信息"""
        user_id = get_jwt_identity()
        user = Profile.query.get(user_id)
        
        if not user:
            return {'message': '用户不存在'}, 404
        
        return user.to_dict(include_sensitive=True), 200
