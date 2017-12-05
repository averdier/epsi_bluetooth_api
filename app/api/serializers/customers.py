# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

customer_post = api.model('Customer post', {
    'last_name': fields.String(required=True, min_length=3, max_length=32, description='Customer last name'),
    'first_name': fields.String(required=True, min_length=3, max_length=32, description='Customer first name'),
    'bluetooth_mac_address': fields.String(required=False, description='Customer bluetooth mac address'),
    'email': fields.String(required=False, min_length=5, max_length=32, description='Customer email address'),
    'phone_number': fields.String(required=False, description='Customer phone number')
})

customer_patch = api.model('Customer patch', {
    'last_name': fields.String(required=False, min_length=3, max_length=32, description='Customer last name'),
    'first_name': fields.String(required=False, min_length=3, max_length=32, description='Customer first name'),
    'bluetooth_mac_address': fields.String(required=False, description='Customer bluetooth mac address'),
    'email': fields.String(required=False, min_length=5, max_length=32, description='Customer email address'),
    'phone_number': fields.String(required=False, description='Customer phone number')
})

customer_minimal = api.model('Customer minimal', {
    'id': fields.String(required=True, description='Customer unique id'),
    'uri': fields.Url('api.customers_customer_item'),
    'last_name': fields.String(required=True, description='Customer last name'),
    'first_name': fields.String(required=True, description='Customer first name'),
})

customer_detail = api.inherit('Customer', customer_minimal, {
    'bluetooth_mac_address': fields.String(required=True, description='Customer bluetooth mac address'),
    'email': fields.String(required=True, min_length=5, max_length=32, description='Customer email address'),
    'phone_number': fields.String(required=True, description='Customer phone number')
})

customer_data_container = api.inherit('Customer data container', {
    'customers': fields.List(fields.Nested(customer_minimal))
})