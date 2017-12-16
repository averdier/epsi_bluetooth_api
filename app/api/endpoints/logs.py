# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.bluetooth_logs import bluetooth_log_data_container
from app.models import User, BluetoothLog

ns = Namespace('logs', description='Logs related operations')

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
#   API deals endpoints
#
# ================================================================================================

@ns.route('/bluetooth')
class BluetoothLogCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(bluetooth_log_data_container)
    def get(self):
        """
        Return logs list
        """
        return {'logs': [log.to_dict(include_id=True) for log in BluetoothLog.search().execute()]}