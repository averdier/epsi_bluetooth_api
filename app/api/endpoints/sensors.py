# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from elasticsearch_dsl import Q
from ..serializers.sensors import sensor_data_container, sensor_post, sensor_patch, sensor_minimal, sensor_detail
from app.models import User, Device

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
        return {'sensors': [sensor.to_dict(include_id=True) for sensor
                            in Device.search().query('term', device_type='sensor').execute()]}

    @ns.marshal_with(sensor_minimal, code=201, description='Sensor successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(sensor_post)
    def post(self):
        """
        Add sensor
        """
        data = request.json

        if len(Device.search().query('term', **{'mqtt_account.username': data['mqtt_account']['username']}).execute()) != 0:
            abort(400, error='MQTT username already exist.')

        sensor = Device(
            device_type='sensor',
            pos_x=data['pos_x'],
            pos_y=data['pos_y'],
            radius=data['radius']
        )
        sensor.hash_key(data['key'])

        data['mqtt_account']['clients_topic'] = 'bluetooth/sensor/' + data['mqtt_account']['username'] + '/from_clients'
        data['mqtt_account']['device_topic'] = 'bluetooth/sensor/' + data['mqtt_account']['username'] + '/from_device'

        sensor.set_mqtt_account(data['mqtt_account'])
        sensor.meta.id = 'sensor_' + str(Device.search().count() + 1)
        sensor.save()

        return sensor.to_dict(include_id=True), 201


@ns.route('/<id>')
@ns.response(404, 'Sensor not found')
class SensorItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(sensor_detail)
    def get(self, id):
        """
        Get sensor
        """
        sensor = Device.get(id=id, ignore=404)

        if sensor is None:
            abort(404, 'Sensor not found.')

        return sensor.to_dict(include_id=True)

    @ns.response(204, 'Sensor successfully patched.')
    @ns.expect(sensor_patch)
    def patch(self, id):
        """
        Patch sensor
        """
        sensor = Device.get(id=id, ignore=404)

        if sensor is None:
            abort(404, 'Sensor not found.')

        data = request.json

        updated = False
        if data.get('mqtt_account', None) is not None:

            if data['mqtt_account'].get('username'):
                sensor_search = Device.search().query('term', **{'mqtt_account.username': data['mqtt_account']['username']}).execute()

                if len(sensor_search) != 0 and sensor_search.hits[0].meta.id != sensor.meta.id:
                    abort(400, error='MQTT username already exist.')
            if sensor.update_mqtt_account(data['mqtt_account']):
                updated = True

        if data.get('key', None) is not None:
            sensor.hash_key(data['key'])
            updated = True

        if data.get('pos_x', None) is not None:
            sensor.pos_x = data['pos_x']
            updated = True

        if data.get('pos_y', None) is not None:
            sensor.pos_y = data['pos_y']
            updated = True

        if data.get('radius', None) is not None:
            sensor.radius = data['radius']
            updated = True

        if updated:
            sensor.update()

        return 'Sensor successfully patched.', 204

    @ns.response(204, 'Sensor successfully deleted.')
    def delete(self, id):
        """
        Delete sensor
        """

        sensor = User.get(id=id, ignore=404)

        if sensor is None:
            abort(404, 'Sensor not found.')

        sensor.delete()

        if Device.get(id=id, ignore=404) is not None:
            abort(400, error='Unable to delete sensor.')

        return 'Sensor successfully deleted.', 204