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
from .endpoints.users import ns as user_namespace
from .endpoints.customers import ns as customer_namespace
from .endpoints.deals import ns as deals_namespace
from .endpoints.sensors import ns as sensors_namespace
from .endpoints.logs import ns as logs_namespace
from .endpoints.tasks import ns as tasks_namespace

api.add_namespace(token_namespace)
api.add_namespace(user_namespace)
api.add_namespace(customer_namespace)
api.add_namespace(deals_namespace)
api.add_namespace(sensors_namespace)
api.add_namespace(logs_namespace)
api.add_namespace(tasks_namespace)
