# -*- coding: utf-8 -*-

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from elasticsearch_dsl import DocType, Date, Text, Integer
from .utils import hash_sha256


class MyDocType(DocType):
    def to_dict(self, include_id=False, include_meta=False):
        base = super().to_dict(include_meta)

        if include_id and not include_meta:
            base['id'] = self.meta.id

        return base


class User(MyDocType):
    """
    User of API
    """

    created_at = Date()
    updated_at = Date()
    username = Text()
    password = Text()
    email = Text()

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


class Sensor(MyDocType):
    device_id = Text()
    created_at = Date()
    updated_at = Date()
