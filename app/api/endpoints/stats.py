# -*- coding: utf-8 -*-

from flask import g, request
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from ..serializers.stats import stats_minimal
from ..parsers import interval_parser
from app.models import User, BluetoothLog, Customer

ns = Namespace('stats', description='Stats related operations')

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
#   API sensors endpoints
#
# ================================================================================================

@ns.route('/')
class StatsItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(stats_minimal)
    @ns.expect(interval_parser)
    def get(self):
        """
        Return stats
        """
        args = interval_parser.parse_args()

        result = {
            'counts': {
                'visitors': 0,
                'customers': 0,
                'logs': 0
            },
            'from_timestamp': args['from'],
            'to_timestamp': args['to']
        }

        result['counts']['logs'] = BluetoothLog.search().filter('range', end_timestamp={
            'gte': args['from'],
            'lte': args['to']
        }).count()

        search = BluetoothLog.search().filter('range', end_timestamp={
            'gte': args['from'],
            'lte': args['to']
        })

        search.aggs.bucket('per_mac', 'terms', field='mac', size=9999)
        response = search.execute()

        mac_addresses = [data.key for data in response.aggregations.per_mac.buckets]

        for mac_address in mac_addresses:
            result['counts']['visitors'] += 1

            if len(Customer.search().query('term', bluetooth_mac_address=mac_address).execute()) != 0:
                result['counts']['customers'] += 1

        return result
