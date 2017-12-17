# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api


counts_model = api.model('Counts', {
    'visitors': fields.Integer(required=True, description='Count of visitors'),
    'customers': fields.Integer(required=True, description='Count of customers'),
    'logs': fields.Integer(required=True, description='Count of logs')
})

stats_minimal = api.model('Stats', {
    'from_timestamp': fields.Float(required=True, description='Stats from timestamp'),
    'to_timestamp': fields.Float(required=True, description='To timestamp'),
    'counts': fields.Nested(counts_model, required=True, description='Stats details')
})