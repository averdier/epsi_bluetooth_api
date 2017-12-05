# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.users import user_data_container, user_post, user_patch, user_minimal, user_detail
from app.models import User

ns = Namespace('users', description='Users related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    Verify auth token

    :param token: User token
    :type token: str

    :return: True if valid token, else False
    :rtype: bool
    """
    user = User.verify_auth_token(token)

    if not user:
        return False

    g.user = user
    return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API users endpoints
#
# ================================================================================================

@ns.route('/')
class UserCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_data_container)
    def get(self):
        """
        Return user list
        """
        pass

    @ns.marshal_with(user_minimal, code=201, description='User successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(user_post)
    def post(self):
        """
        Add user
        """
        pass


@ns.route('/<id>')
@ns.response(404, 'User not found')
class UserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_detail)
    def get(self, id):
        """
        Get user
        """
        pass

    @ns.response(204, 'User successfully patched.')
    @ns.expect(user_patch)
    def patch(self, id):
        """
        Patch user
        """
        pass

    @ns.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Delete user
        """