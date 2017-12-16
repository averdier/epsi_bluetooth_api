# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


sensor_data_minimal = api.model('Sensor data minimal', {
    'device_id': fields.String(required=True, description='Sensor unique ID'),
    'rssi': fields.String(required=True, description='Signal strength'),
    'start_timestamp': fields.Float(required=True, description='Start timestamp'),
    'end_timestamp': fields.Float(required=True, description='End timestamp')
})

bluetooth_log_minimal = api.model('Bluetooth log minimal', {
    'start_timestamp': fields.Float(required=True, description='Min start timestamp'),
    'end_timestamp': fields.Float(required=True, description='Max start timestamp'),
    'mac': fields.String(required=True, description='Bluetooth mac address'),
    'sensors_data': fields.Nested(sensor_data_minimal, required=True, description='Sensors data')
})


bluetooth_log_data_container = api.model('Bluetooth log data container', {
    'logs': fields.List(fields.Nested(bluetooth_log_minimal), required=True, description='Bluetooth logs')
})