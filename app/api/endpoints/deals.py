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
        return {'deals': [deal.to_dict(include_id=True) for deal in Deal.search().execute()]}

    @ns.marshal_with(deal_minimal, code=201, description='Deal successfully added.')
    @ns.doc(response={
        400: 'Validation error'
    })
    @ns.expect(deal_post)
    def post(self):
        """
        Add deal
        """
        data = request.json

        deal = Deal(
            label=data['label'],
            start_at=data['start_at'],
            end_at=data['end_at']
        )

        if data.get('description', None) is not None:
            deal.description = data['description']

        deal.save()

        return deal.to_dict(include_id=True), 201


@ns.route('/<id>')
@ns.response(404, 'Deal not found')
class DealItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(deal_detail)
    def get(self, id):
        """
        Get deal
        """
        deal = Deal.get(id=id, ignore=404)

        if deal is None:
            abort(404, 'Deal not found.')

        return deal.to_dict(include_id=True)

    @ns.response(204, 'Deal successfully patched.')
    @ns.expect(deal_patch)
    def patch(self, id):
        """
        Patch deal
        """
        deal = Deal.get(id=id, ignore=404)

        if deal is None:
            abort(404, 'Deal not found.')

        data = request.json
        updated = True

        if data.get('label', None) is not None:
            deal.label = data['label']
            updated = True

        if data.get('description', None) is not None:
            deal.description = data['description']
            updated = True

        if data.get('start_at', None) is not None:
            deal.start_at = data['start_at']
            updated = True

        if data.get('end_at', None) is not None:
            deal.end_at = data['end_at']
            updated = True

        if updated:
            deal.save()

        return 'Deal successfully patched.', 204

    @ns.response(204, 'Deal successfully deleted.')
    def delete(self, id):
        """
        Delete deal
        """

        deal = Deal.get(id=id, ignore=404)

        if deal is None:
            abort(404, 'Deal not found.')

        deal.delete()

        if Deal.get(id=id, ignore=404) is not None:
            abort(400, error='Unable to delete deal.')

        return 'Deal successfully deleted.', 204