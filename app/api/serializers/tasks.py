# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


task_status = api.model('Task status', {
    'status': fields.String(required=True, description='Task status'),
    'state': fields.String(required=True, description='Task state'),
    'current': fields.Integer(required=True, description='Current step'),
    'total': fields.Integer(required=True, description='Total steps'),
    'message': fields.String(required=True, description='Task message')
})

send_options = api.model('Send option', {
    'email': fields.Boolean(required=True, default=False, description='Send email'),
    'sms': fields.Boolean(required=True, default=False, description='Send sms')
})

send_task_parameters = api.model('Send task parameters', {
    'send_options': fields.Nested(send_options, required=True, description='Send options'),
    'time_threshold': fields.Integer(required=True, min=0, default=1, description='Time threshold since now'),
    'deal_id': fields.String(required=True, description='Deal unique ID')
})

send_task_response = api.model('Send task response', {
    'task_id': fields.String(required=True, description='Task id'),
    'uri': fields.Url('manage.tasks_send_deal_task_status', required=True, description='Task status uri')
})

