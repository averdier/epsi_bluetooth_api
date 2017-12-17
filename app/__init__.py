# -*- coding: utf-8 -*-

from flask import Flask, request
from celery import Celery
from flask_cors import CORS
from config import config
from elasticsearch_dsl.connections import connections
from .extensions import mail

CELERY_TASK_LIST = [
    'app.tasks'
]


def create_celery_app(app=None, config_name='default'):
    """
    Create Celery app

    :param app:
    :param config_name:

    :return: Celery app
    """
    app = app or create_app(config_name)
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        include=CELERY_TASK_LIST
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(config_name='default'):
    """
    Create Flask app

    :param config_name:
    :return: Flask
    """

    from .api import blueprint as api_blueprint

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    connections.create_connection(hosts=[config[config_name].ELASTICSEARCH_HOST], timeout=20)

    from app.models import User, Customer, Deal, Device, BluetoothLog
    with app.app_context():
        User.init()
        Customer.init()
        Deal.init()
        Device.init()
        BluetoothLog.init()

        user_search = User.search().execute()

        if len(user_search) == 0:
            user = User(username='averdier')
            user.hash_password('averdier')
            user.save()

    app.register_blueprint(api_blueprint)

    extensions(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    return app


def extensions(app):
    mail.init_app(app)
