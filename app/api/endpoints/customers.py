# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.customers import customer_data_container, customer_post, customer_patch, customer_minimal, \
    customer_detail
from app.models import User, Customer

ns = Namespace('customers', description='Customers related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    Verify auth token

    :param token: User token
    :type token: str

    :return: True if valid token, else False
    :rtype: bool
    """
    user = User.verify_auth_token(token)

    if not user:
        return False

    g.user = user
    return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API customers endpoints
#
# ================================================================================================

@ns.route('/')
class CustomerCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(customer_data_container)
    def get(self):
        """
        Return customer list
        """
        pass

    @ns.marshal_with(customer_minimal, code=201, description='Customer successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(customer_post)
    def post(self):
        """
        Add customer
        """
        pass


@ns.route('/<id>')
@ns.response(404, 'Customer not found')
class CustomerItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(customer_detail)
    def get(self, id):
        """
        Get customer
        """
        pass

    @ns.response(204, 'Customer successfully patched.')
    @ns.expect(customer_patch)
    def patch(self, id):
        """
        Patch customer
        """
        pass

    @ns.response(204, 'Customer successfully deleted.')
    def delete(self, id):
        """
        Delete customer
        """