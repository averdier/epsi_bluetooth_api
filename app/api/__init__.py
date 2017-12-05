# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restplus import Api


authorizations = {
    'tokenKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'basicAuth': {
        'type': 'basic',
        'in': 'header'
    }
}

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='EPSI Bluetooth API',
          version='0.1',
          description='EPSI Bluetooth Manage API',
          authorizations=authorizations,
          security='tokenKey'
          )


from .endpoints.token import ns as token_namespace


api.add_namespace(token_namespace)
