# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

mqtt_account_post = api.model('MQTT account post', {
    'username': fields.String(required=True, min_length=3, max_length=32, description='MQTT username'),
    'password': fields.String(required=True, min_length=3, max_length=32, description='MQTT password'),
    'server': fields.String(required=True, min_length=3, max_length=64, default='93.118.34.190', description='MQTT server address'),
    'port': fields.Integer(required=True, default=1883, description='MQTT server port'),
    'keep_alive': fields.Integer(required=True, default=60, description='MQTT keep alive')
})

mqtt_account_patch = api.model('MQTT account patch', {
    'username': fields.String(required=False, min_length=3, max_length=32, description='MQTT username'),
    'password': fields.String(required=False, min_length=3, max_length=32, description='MQTT password'),
    'server': fields.String(required=False, min_length=3, max_length=64, default='93.118.34.190', description='MQTT server address'),
    'port': fields.Integer(required=False, default=1883, description='MQTT server port'),
    'keep_alive': fields.Integer(required=False, default=60, description='MQTT keep alive'),
    'clients_topic': fields.String(required=False, min_length=3, max_length=64, description='Clients topic'),
    'device_topic': fields.String(required=False, min_length=3, max_length=64, description='Device topic')
})

mqtt_account = api.model('MQTT account', {
    'username': fields.String(required=True, description='MQTT username'),
    'password': fields.String(required=True, description='MQTT password'),
    'server': fields.String(required=True, description='MQTT server address'),
    'port': fields.Integer(required=True, description='MQTT server port'),
    'keep_alive': fields.Integer(required=True, description='MQTT keep alive'),
    'clients_topic': fields.String(required=True, description='Clients topic'),
    'device_topic': fields.String(required=True, description='Device topic')
})

sensor_post = api.model('Sensor post', {
    'key': fields.String(required=True, min_length=3, max_length=16, description='Sensor key'),
    'pos_x': fields.Integer(required=True, description='Sensor X position'),
    'pos_y': fields.Integer(required=True, description='Sensor Y position'),
    'radius': fields.Integer(required=True, exclusiveMin=0, description='Sensor radius'),
    'mqtt_account': fields.Nested(mqtt_account_post, required=True, description='MQTT account')
})

sensor_patch = api.model('Sensor patch', {
    'mqtt_account': fields.Nested(mqtt_account_patch, required=False, description='MQTT account'),
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
    'mqtt_account': fields.Nested(mqtt_account, required=True, description='MQTT account'),
})

sensor_data_container = api.inherit('Sensor data container', {
    'sensors': fields.List(fields.Nested(sensor_minimal))
})
