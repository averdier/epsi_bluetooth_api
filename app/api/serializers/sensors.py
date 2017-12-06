# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

sensor_post = api.model('Sensor post', {
    'device_id': fields.String(required=True, description='MQTT device_id'),
    'mqtt_token': fields.String(required=False, description='MQTT token'),
    'key': fields.String(required=True, min_length=3, max_length=16, description='Sensor key'),
    'pos_x': fields.Integer(required=True, description='Sensor X position'),
    'pos_y': fields.Integer(required=True, description='Sensor Y position'),
    'radius': fields.Integer(required=True, exclusiveMin=0, description='Sensor radius'),
})

sensor_patch = api.model('Sensor patch', {
    'mqtt_token': fields.String(required=False, description='MQTT token'),
    'key': fields.String(required=False, min_length=3, max_length=16, description='Sensor key'),
    'pos_x': fields.Integer(required=False, description='Sensor X position'),
    'pos_y': fields.Integer(required=False, description='Sensor Y position'),
    'radius': fields.Integer(required=False, exclusiveMin=0, description='Sensor radius')
})

sensor_minimal = api.model('Sensor minimal', {
    'id': fields.String(required=True, description='Sensor unique id'),
    'uri': fields.Url('api.sensors_sensor_item'),
    'pos_x': fields.Integer(required=True, description='Sensor X position'),
    'pos_y': fields.Integer(required=True, description='Sensor Y position'),
    'radius': fields.Integer(required=True, exclusiveMin=0, description='Sensor radius')
})

sensor_detail = api.inherit('Sensor', sensor_minimal, {
    'mqtt_token': fields.String(required=True, description='MQTT token'),
})

sensor_data_container = api.inherit('Sensor data container', {
    'sensors': fields.List(fields.Nested(sensor_minimal))
})
