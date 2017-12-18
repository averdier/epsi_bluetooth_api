# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

user_post = api.model('User post', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='User username'),
    'password': fields.String(required=True, min_length=3, max_length=32, description='User password'),
    'email': fields.String(required=True, min_length=5, max_length=32, description='User email address')
})

user_patch = api.model('User patch', {
    'password': fields.String(required=False, min_length=3, max_length=32, description='User password'),
    'email': fields.String(required=False, min_length=5, max_length=32, description='User email address')
})

user_minimal = api.model('User minimal', {
    'id': fields.String(required=True, description='User unique id'),
    'uri': fields.Url('api.users_user_item'),
    'username': fields.String(required=True, description='User username')
})

user_detail = api.inherit('User', user_minimal, {
    'email': fields.String(required=True, description='User email address')
})

user_data_container = api.inherit('User data container', {
    'users': fields.List(fields.Nested(user_minimal))
})