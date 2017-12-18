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
        return {'users': [user.to_dict(include_id=True) for user in User.search().execute()]}

    @ns.marshal_with(user_minimal, code=201, description='User successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(user_post)
    def post(self):
        """
        Add user
        """
        data = request.json

        if len(User.search().query('match', username=data['username']).execute()) != 0:
            abort(400, error='Username already exist.')

        if len(User.search().query('match', email=data['email']).execute()) != 0:
            abort(400, error='Email already exist.')

        user = User(
            username=data['username'],
            email=data['email']
        )
        user.hash_password(data['password'])
        user.save()

        return user.to_dict(include_id=True), 201


@ns.route('/<id>')
@ns.response(404, 'User not found.')
class UserItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(user_detail)
    def get(self, id):
        """
        Get user
        """
        user = User.get(id=id, ignore=404)

        if user is None:
            abort(404, 'User not found.')

        return user.to_dict(include_id=True)

    @ns.response(204, 'User successfully patched.')
    @ns.expect(user_patch)
    def patch(self, id):
        """
        Patch user
        """
        user = User.get(id=id, ignore=404)

        if user is None:
            abort(404, 'User not found.')

        data = request.json

        updated = False
        if data.get('password', None) is not None:
            user.hash_password(data['password'])
            updated = True

        if data.get('email', None) is not None:
            user_search = User.search().query('match', email=data['email']).execute()

            if len(user_search) > 0:
                if user_search.hits[0].meta.id != id:
                    abort(400, error='Email already exist.')

            user.email = data['email']
            updated = True

        if updated:
            user.save()

        return 'User successfully patched.', 204

    @ns.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Delete user
        """

        user = User.get(id=id, ignore=404)

        if user is None:
            abort(404, 'User not found.')

        user.delete()

        if User.get(id=id, ignore=404) is not None:
            abort(400, error='Unable to delete user.')

        return 'User successfully deleted.', 204
