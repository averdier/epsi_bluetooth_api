# -*- coding: utf-8 -*-

from . import api

log_parser = api.parser()
log_parser.add_argument('mac', required=False, type=str, help='Mac address')
log_parser.add_argument('since', required=False, type=int, help='Since timestamp')

interval_parser = api.parser()
interval_parser.add_argument('from', required=True, type=int, help='From timestamp')
interval_parser.add_argument('to', required=True, type=int, help='To timestamp')
