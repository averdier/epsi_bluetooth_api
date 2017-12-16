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
        return {'customers': [customer.to_dict(include_id=True) for customer in Customer.search().execute()]}

    @ns.marshal_with(customer_minimal, code=201, description='Customer successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(customer_post)
    def post(self):
        """
        Add customer
        """
        data = request.json

        customer = Customer(
            last_name=data['last_name'],
            first_name=data['first_name']
        )

        if data.get('email', None) is not None:
            if len(Customer.search().query('match', email=data['email']).execute()) != 0:
                abort(400, error='Email already exist.')

            customer.email = data['email']

        if data.get('phone_number', None) is not None:
            if len(Customer.search().query('match', phone_number=data['phone_number']).execute()) != 0:
                abort(400, error='Phone number already exist.')

            customer.phone_number = data['phone_number']

        if data.get('bluetooth_mac_address', None) is not None:
            if len(Customer.search().query('match', bluetooth_mac_address=data['bluetooth_mac_address']).execute()) != 0:
                abort(400, error='Bluetooth mac address already exist.')

            customer.bluetooth_mac_address = data['bluetooth_mac_address']

        customer.save()

        return customer.to_dict(include_id=True), 201


@ns.route('/<id>')
@ns.response(404, 'Customer not found')
class CustomerItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(customer_detail)
    def get(self, id):
        """
        Get customer
        """
        customer = Customer.get(id=id, ignore=404)

        if customer is None:
            abort(404, 'Customer not found.')

        return customer.to_dict(include_id=True)

    @ns.response(204, 'Customer successfully patched.')
    @ns.expect(customer_patch)
    def patch(self, id):
        """
        Patch customer
        """
        customer = Customer.get(id=id, ignore=404)

        if customer is None:
            abort(404, 'Customer not found.')

        data = request.json
        updated = False
        if data.get('email', None) is not None:
            email_search = Customer.search().query('match', email=data['email']).execute()
            if len(email_search) > 0 and email_search.hits[0].meta.id != id:
                abort(400, error='Email already exist.')

            customer.email = data['email']
            updated = True

        if data.get('phone_number', None) is not None:
            phone_search = Customer.search().query('match', phone_number=data['phone_number']).execute()
            if len(phone_search) != 0 and phone_search.hits[0].meta.id != id:
                abort(400, error='Phone number already exist.')

            customer.phone_number = data['phone_number']
            updated = True

        if data.get('bluetooth_mac_address', None) is not None:
            mac_address_search = Customer.search().query('match', bluetooth_mac_address=data['bluetooth_mac_address']).execute()
            if len(mac_address_search) > 0 and mac_address_search.hits[0].meta.id != id:
                abort(400, error='Bluetooth mac address already exist.')

            customer.bluetooth_mac_address = data['bluetooth_mac_address']
            updated = True

        if data.get('last_name', None) is not None:
            customer.last_name = data['last_name']
            updated = True

        if data.get('first_name', None) is not None:
            customer.first_name = data['first_name']
            updated = True

        if updated:
            customer.save()

        return 'Customer successfully patched.', 204

    @ns.response(204, 'Customer successfully deleted.')
    def delete(self, id):
        """
        Delete customer
        """

        customer = Customer.get(id=id, ignore=404)

        if customer is None:
            abort(404, 'Customer not found.')

        customer.delete()

        if Customer.get(id=id, ignore=404) is not None:
            abort(400, error='Unable to delete customer.')

        return 'Customer successfully deleted.', 204