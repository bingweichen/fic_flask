#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import g
from flask_restplus import Resource, Namespace, fields
from app.user.service import login, register, get_all
from common.decorators import arguments_parser, catch_error
from common.responses import created, ok
from app.user.model import User
from flask_restplus import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate to charge for this resource',
                    required=True
                    )

api = Namespace('auth', path='/auth')
login_model = api.model('login', {
    'username': fields.String(required=True, description='user username'),
    'password': fields.String(required=True, description='user password '),
})

register_model = api.model('register', {
    'username': fields.String(required=True, description='user username'),
    'password': fields.String(required=True, description='user password'),
})

user_model = api.model('user', {
    'id': fields.String(required=True, description='user username'),
    'username': fields.String(required=True, description='user username'),
})


@api.route('/login')
class LoginResource(Resource):
    """User Login Resource"""

    @api.doc(description='user login')
    @api.expect(login_model, validate=True)
    @arguments_parser
    @catch_error
    def post(self):
        """用户登录"""
        data = g.args
        result = login(username=data.get("username"), password=data.get("password"))
        return result


@api.route('/users')
class UsersResource(Resource):
    @api.response(201, 'User successfully created.')
    @api.doc('create new user')
    @api.expect(register_model, validate=True)
    @catch_error
    @arguments_parser
    def post(self):
        """用户注册"""
        register(g.args)
        return created('Successfully registered!')

    @api.marshal_with(user_model)
    def get(self):
        """获取所有用户"""
        users = User.query.filter_by().all()
        return users


@api.response(404, 'User not found')
@api.route('/users/<string:user_id>')
class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        """获取单个用户"""
        return User.query.filter_by(id=user_id).first()

