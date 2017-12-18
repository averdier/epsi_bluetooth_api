# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

deal_post = api.model('Deal post', {
    'label': fields.String(required=True, min_length=3, max_length=32, description='Deal label'),
    'description': fields.String(required=False, min_length=3, max_length=32, description='Deal description'),
    'start_at': fields.DateTime(required=True, dt_format='iso8601', description='Deal start datetime'),
    'end_at': fields.DateTime(required=True, dt_format='iso8601', description='Deal start datetime'),
})

deal_patch = api.model('Deal patch', {
    'label': fields.String(required=False, min_length=3, max_length=32, description='Deal label'),
    'description': fields.String(required=False, min_length=3, max_length=32, description='Deal description'),
    'start_at': fields.DateTime(required=False, dt_format='iso8601', description='Deal start datetime'),
    'end_at': fields.DateTime(required=False, dt_format='iso8601', description='Deal start datetime'),
})

deal_minimal = api.model('Deal minimal', {
    'id': fields.String(required=True, description='Deal unique id'),
    'uri': fields.Url('api.deals_deal_item'),
    'label': fields.String(required=True, description='Deal label'),
    'start_at': fields.DateTime(required=True, dt_format='iso8601', description='Deal start datetime'),
    'end_at': fields.DateTime(required=True, dt_format='iso8601', description='Deal start datetime')
})

deal_detail = api.inherit('Deal', deal_minimal, {
    'description': fields.String(required=True, description='Deal description')
})

deal_data_container = api.inherit('Deal data container', {
    'deals': fields.List(fields.Nested(deal_minimal))
})