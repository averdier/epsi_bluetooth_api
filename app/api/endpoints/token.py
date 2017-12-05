# -*- coding: utf-8 -*-

from flask import g
from flask_restplus import Namespace, Resource
from flask_httpauth import HTTPBasicAuth
from ..serializers import auth_token
from app.models import User

ns = Namespace('token', description='Token related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """
    Verify User authorization

    :param username: Unique username
    :type username: str

    :param password: User password
    :type password: str

    :return: True if user can connect, else False
    :rtype: bool
    """
    user_search = User.search().query('match', username=username).execute()

    if len(user_search) == 0 or not user_search.hits[0].verify_password(password):
        return False

    g.user = user_search.hits[0]
    return True

# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API token endpoints
#
# ================================================================================================


@ns.route('/')
class TokenResource(Resource):
    decorators = [auth.login_required]

    @ns.doc(security='basicAuth')
    @ns.marshal_with(auth_token)
    def get(self):
        """
        Return auth token
        """

        token = g.user.generate_auth_token()

        return {'token': token.decode('ascii')}