# -*- coding: utf-8 -*-

import time
from flask import current_app
from flask_mail import Message
from . import create_celery_app
from .models import Deal, BluetoothLog, Customer
from .extensions import mail

celery = create_celery_app()


@celery.task(bind=True)
def send_deal(self, args):
    meta = {
        'status': 'RUNNING',
        'current': 0,
        'total': 3,
        'message': 'Searching presents customers'
    }
    self.update_state(state='PROGRESS', meta=meta)

    now = time.time()
    gte = now - 60 * args['time_threshold']

    mac_addresses_search = BluetoothLog.search().filter('range', end_timestamp={'gte': gte})
    mac_addresses_search.aggs.bucket('per_mac', 'terms', field='mac', size=1000)

    response = mac_addresses_search.execute()
    mac_addresses = [result.key for result in response.aggregations.per_mac.buckets]
    print(mac_addresses)

    meta['current'] += 1
    meta['message'] = 'Searching customers'
    self.update_state(state='PROGRESS', meta=meta)

    customers = []
    for mac_address in mac_addresses:
        customers_search = Customer.search().query('term', bluetooth_mac_address=mac_address).execute()

        for customer in customers_search:
            if customer not in customers:
                customers.append(customer)

    meta['current'] += 1
    meta['message'] = 'Sending deal'
    self.update_state(state='PROGRESS', meta=meta)

    emails = []
    numbers = []

    for customer in customers:
        if customer.email and customer.email != '':
            emails.append(customer.email)

        if customer.phone_number and customer.phone_number != '':
            numbers.append(customer.phone_number)

    if args['send_options']['email']:
        with current_app.app_context():

            with mail.connect() as conn:

                for email in emails:

                    print(email)

                    message = args['deal']['description']
                    subject = args['deal']['label']

                    msg = Message(
                        recipients=[email],
                        body=message,
                        subject=subject
                    )

                    conn.send(msg)

    meta['current'] += 1
    meta['status'] = 'SUCCESS'
    meta['message'] = 'Deal successfully sent'
    self.update_state(state='SUCCESS', meta=meta)

    return meta

