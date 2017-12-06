# -*- coding: utf-8 -*-

from flask import Flask
from config import config
from elasticsearch_dsl.connections import connections


def create_app(config_name='default'):
    """
    Create Flask app

    :param config_name:
    :return: Flask
    """

    from .api import blueprint as api_blueprint

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    connections.create_connection(hosts=[config[config_name].ELASTICSEARCH_HOST], timeout=20)

    from app.models import User, Customer, Deal, Sensor
    with app.app_context():
        User.init()
        Customer.init()
        Deal.init()
        Sensor.init()

        user_search = User.search().execute()

        if len(user_search) == 0:
            user = User(username='averdier')
            user.hash_password('averdier')
            user.save()

    app.register_blueprint(api_blueprint)

    return app