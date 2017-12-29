# -*- coding: utf-8 -*-

import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration
    """
    SECRET_KEY = os.environ.get('EPSI_KEY') or 'abcdefghijk'
    TOKEN_EXPIRATION_TIME = 6000
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    CELERY_BROKER_URL = ''
    CELERY_RESULT_BACKEND = ''

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''

    NEXMO_KEY = ''
    NEXMO_SECRET = ''
    SMS_FROM = ''

    @staticmethod
    def init_app(app):
        """
        Init app

        :param app: Flask App
        :type app: Flask
        """
        pass


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    ELASTICSEARCH_HOST = "localhost"
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = True


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    ELASTICSEARCH_HOST = "localhost"
    RESTPLUS_MASK_SWAGGER = True
    RESTPLUS_ERROR_404_HELP = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}