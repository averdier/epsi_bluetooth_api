# -*- coding: utf-8 -*-

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from elasticsearch_dsl import DocType, Date, Text, Integer, Keyword, InnerObjectWrapper, Object
from .utils import hash_sha256


class MyDocType(DocType):
    created_at = Date()
    updated_at = Date()

    def to_dict(self, include_id=False, include_meta=False):
        base = super().to_dict(include_meta)

        if include_id and not include_meta:
            base['id'] = self.meta.id

        return base

    def save(self, **kwargs):
        self.created_at = datetime.utcnow()
        return super().save(**kwargs)

    def update(self, using=None, index=None, **fields):
        self.updated_at = datetime.utcnow()
        return super().update(using, index, **fields)


class User(MyDocType):
    """
    User of API
    """

    username = Keyword()
    password = Keyword()
    email = Keyword()

    class Meta:
        index = 'bluetooth'

    def hash_password(self, password):
        """
        Set new user passsword

        :param password: New password to hash
        :type password: str
        """
        self.password = hash_sha256(password)

    def verify_password(self, password, verify_hash=True):
        """
        Verify if password is user password

        :param password: Password to test
        :type password: str
        :param verify_hash: Verify hash of password or not (default True)
        :type verify_hash: bool

        :return: True if is user password, False else
        :rtype: bool
        """

        if verify_hash:
            return self.password == hash_sha256(password)
        else:
            return self.password == password

    def generate_auth_token(self, expiration=None):
        """
        Generate token for user authentification

        :param expiration: Auth expiration
        :type expiration: int

        :return: Auth token
        :rtype: str
        """

        if expiration is None:
            expiration = current_app.config['TOKEN_EXPIRATION_TIME']

        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return serializer.dumps({'id': self.meta.id})

    @staticmethod
    def verify_auth_token(token):
        """
        Return user form token

        :param token: Token
        :type token: str

        :return: User if valid token, else None
        :rtype: User|None
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = serializer.loads(token)
        except SignatureExpired:
            print('SignatureExpired')
            return None
        except BadSignature:
            print('BadSignature')
            return None

        user = User.get(id=data['id'], ignore=404)

        return user


class Customer(MyDocType):
    """
    Customer
    """
    last_name = Text()
    first_name = Text()
    bluetooth_mac_address = Keyword()
    email = Keyword()
    phone_number = Keyword()

    class Meta:
        index = 'bluetooth'


class Deal(MyDocType):
    label = Text()
    description = Text()
    start_at = Date()
    end_at = Date()

    class Meta:
        index = 'bluetooth'


class MQTTAccount(InnerObjectWrapper):
    """
    MQTT Account wrapper
    """


class Device(MyDocType):
    device_type = Keyword()
    pos_x = Integer()
    pos_y = Integer()
    radius = Integer()
    key = Keyword()
    mqtt_account = Object(
        doc_class=MQTTAccount,
        properties={
            'username': Keyword(),
            'password': Keyword(),
            'server': Keyword(),
            'port': Integer(),
            'keep_alive': Keyword(),
            'clients_topic': Keyword(),
            'response_topic': Keyword()
        }
    )

    class Meta:
        index = 'bluetooth'

    def set_mqtt_account(self, args):
        self.mqtt_account = {
            'username': args['username'],
            'password': args['password'],
            'server': args['server'],
            'port': args['port'],
            'keep_alive': args['keep_alive'],
            'clients_topic': args['clients_topic'],
            'device_topic': args['device_topic']
        }

    def update_mqtt_account(self, args):
        updated = False

        if args.get('username'):
            self.mqtt_account.username = args['username']
            updated = True

        if args.get('password'):
            self.mqtt_account.password = args['password']
            updated = True

        if args.get('server'):
            self.mqtt_account.server = args['server']
            updated = True

        if args.get('port'):
            self.mqtt_account.port = args['port']
            updated = True

        if args.get('keep_alive'):
            self.mqtt_account.keep_alive = args['keep_alive']
            updated = True

        if args.get('clients_topic'):
            self.mqtt_account.clients_topic = args['clients_topic']
            updated = True

        if args.get('device_topic'):
            self.mqtt_account.device_topic = args['device_topic']
            updated = True

        return updated

    def hash_key(self, key):
        """
        Set new device key

        :param key: New key to hash
        :type key: str
        """
        self.key = hash_sha256(key)
