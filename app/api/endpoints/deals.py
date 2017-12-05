# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.deals import deal_data_container, deal_post, deal_patch, deal_minimal, deal_detail
from app.models import User, Deal

ns = Namespace('deals', description='Deals related operations')

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
#   API deals endpoints
#
# ================================================================================================

@ns.route('/')
class DealCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(deal_data_container)
    def get(self):
        """
        Return deal list
        """
        pass

    @ns.marshal_with(deal_minimal, code=201, description='Deal successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(deal_post)
    def post(self):
        """
        Add deal
        """
        pass


@ns.route('/<id>')
@ns.response(404, 'Deal not found')
class DealItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(deal_detail)
    def get(self, id):
        """
        Get deal
        """
        pass

    @ns.response(204, 'Deal successfully patched.')
    @ns.expect(deal_patch)
    def patch(self, id):
        """
        Patch deal
        """
        pass

    @ns.response(204, 'Deal successfully deleted.')
    def delete(self, id):
        """
        Delete deal
        """