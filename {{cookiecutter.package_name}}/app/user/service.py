#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, g
import uuid
import jwt
import datetime
from functools import wraps

from app.user.model import User, BlackList
from common.mixins import DictMixin
from common.responses import unauthorized
from common.errors import (TokenBlackListedError,
                           ExpiredSignatureError,
                           InvalidTokenError,
                           TokenMissedError,
                           UserDoesNotExistError,
                           NotMatchOrUserDoesNotExistsError,
                           UserAlreadyExistError)
from config import Config


def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = generate_token(user.id)
        if token:
            result = {
                'message': 'Successfully logged in.',
                'Authorization': token.decode('utf-8'),
                'user_name': user.username
            }
            return result
    else:
        raise NotMatchOrUserDoesNotExistsError


def logout(authorization_header):
    token = authorization_header.split(" ")[1] if authorization_header else ''
    if token:
        resp = decode_token(token)
        if not isinstance(resp, str):
            add_token_to_blacklist(token=token)
    else:
        raise InvalidTokenError


def add_token_to_blacklist(token):
    blacklist = BlackList(token)
    blacklist.add()


def register(data):
    user = User.query.filter_by(username=data.get('username', None)).first()
    if not user:
        new_user = DictMixin.from_dict(User, data)
        new_user.password = data.get('password')
        return new_user.add()
    else:
        raise UserAlreadyExistError


def get_all():
    users = User.query.filter_by().all()
    users_json = []
    for u in users:
        user_dict = u.as_dict()
        del user_dict["password_hash"]
        users_json.append(user_dict)
    return users_json

# def get_all_users()


def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY)
        is_blacklisted_token = BlackList.check_blacklist(token)
        if is_blacklisted_token:
            raise TokenBlackListedError
        else:
            return payload['sub']
    except ExpiredSignatureError:
        raise ExpiredSignatureError
    except InvalidTokenError:
        raise InvalidTokenError


def current_user(current_request):
    authorization_header = current_request.headers.get('Authorization')
    if authorization_header:
        token = authorization_header.split(" ")[1]
    else:
        raise TokenMissedError

    if token:
        user_id = decode_token(token)
        user = User.query.filter(User.id == user_id).first()
        if not user:
            raise UserDoesNotExistError
        return user.id
    else:
        raise InvalidTokenError


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            user_info = current_user(request)
            # save user information to flask g variable
            g.user = user_info
            return func(*args, **kwargs)
        except TokenMissedError as e:
            return unauthorized(e.message)
        except TokenBlackListedError as e:
            return unauthorized(e.message)
        except ExpiredSignatureError:
            return unauthorized('Token is expired, please try to login again!')
        except InvalidTokenError:
            return unauthorized('Invalid token, please try to login again!')
        except UserDoesNotExistError:
            return unauthorized("User does not exist")

    return decorated
