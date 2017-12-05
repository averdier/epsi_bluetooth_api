# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.sensors import sensor_data_container, sensor_post, sensor_patch, sensor_minimal, sensor_detail
from app.models import User, Sensor

ns = Namespace('sensors', description='Sensors related operations')

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
#   API sensors endpoints
#
# ================================================================================================

@ns.route('/')
class SensorCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(sensor_data_container)
    def get(self):
        """
        Return sensor list
        """
        pass

    @ns.marshal_with(sensor_minimal, code=201, description='Sensor successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(sensor_post)
    def post(self):
        """
        Add sensor
        """
        pass


@ns.route('/<id>')
@ns.response(404, 'Sensor not found')
class SensorItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(sensor_detail)
    def get(self, id):
        """
        Get sensor
        """
        pass

    @ns.response(204, 'Sensor successfully patched.')
    @ns.expect(sensor_patch)
    def patch(self, id):
        """
        Patch sensor
        """
        pass

    @ns.response(204, 'Sensor successfully deleted.')
    def delete(self, id):
        """
        Delete sensor
        """