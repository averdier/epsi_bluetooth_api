# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.tasks import task_status, send_task_parameters, send_task_response
from app.models import User, Deal

ns = Namespace('tasks', description='Tasks related operations')

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
#   API tasks endpoints
#
# ================================================================================================

@ns.route('/deals/send')
@ns.response(404, 'Deal not found.')
class SendDealTask(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(send_task_response, code=201, description='Task successfully added.')
    @ns.expect(send_task_parameters)
    def post(self):
        """
        Add send deal task
        """
        data = request.json

        deal = Deal.get(id=data['deal_id'], ignore=404)
        if deal is None:
            abort(404, 'Deal not found')

        pass


@ns.route('/deals/send/<task_id>')
@ns.response(404, 'Task not found')
class SendDealTaskStatus(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(task_status)
    def get(self, task_id):
        """
        Send task status
        """
        pass
