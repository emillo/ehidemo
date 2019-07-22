# -*- coding: utf-8 -*-
import logging
import json

from urllib.parse import urlparse, parse_qs  # , urlencode
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path

from .database import Database

curpath = path.dirname(path.realpath(__file__))
parentpath = path.dirname(curpath)
db = Database(path.join(parentpath, 'ehidemo.db'))
logfile = path.join(parentpath, 'ehidemo.log')

logging.basicConfig(filename=logfile, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class DAO:
    def __init__(self):
        self.customers = db.get_customers()
        logging.info('initialized customer list')

    def add_notification(self, notification_label, payload):
        customer_id = self.get_customer_id(notification_label)
        payload = self.truncate_payload(payload)
        if customer_id:
            result = db.add_notification(payload, customer_id)
        else:
            result = (False, "label '" +
                      notification_label + "' not found!")
        return result

    def add_stray_notification(self, payload):
        return db.add_stray_notification(payload)

    def refresh_customers(self):
        self.customers = db.get_customers()

    def get_customer_id(self, notification_label):
        for customer in self.customers:
            if customer.notification_label.lower() == \
               notification_label.lower():
                return str(customer.id)
        return None

    def truncate_payload(self, payload):
        return payload[:300]


DAO = DAO()


class InputValidator():
    required_fields = ('label', 'payload')

    def is_input_valid(self, qs_fields):
        for field in self.required_fields:
            if field not in qs_fields:
                message = "Input error: field '" + field + "' missing"
                return (False, message)
            if 'payload' in qs_fields and (len(qs_fields['payload']) > 1):
                message = "Input error: only one payload allowed"
                return (False, message)
        return (True, None)


validator = InputValidator()


class HTTPHandler(BaseHTTPRequestHandler):

    def set_headers(self, status, content_type="application/json"):
        self.send_response(status)
        self.send_header('content-type', content_type)
        self.end_headers()

    def do_GET(self):
        message = "GET request: " + self.path
        logging.debug(message)
        qs_fields = parse_qs(urlparse(self.path).query)
        validation = validator.is_input_valid(qs_fields)
        if(validation[0]):
            payload = str(qs_fields['payload'][0])

            if(len(qs_fields['label']) == 1):
                label = qs_fields['label'][0]
                result = DAO.add_notification(label, payload)
            else:
                logging.warning('notification with multiple labels!')
                result = DAO.add_stray_notification(payload)

            if (result[0]):
                self.set_headers(200)
                response = {
                    "status": "ok",
                    "notification": result[1]
                }
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                logging.info(result[1])
            else:
                self.error_message(result[1])
                logging.error(self.path + ' - ' + result[1])
        else:
            self.error_message(validation[1])
            logging.error(self.path + ' - ' + validation[1])

    def error_message(self, message):
        self.set_headers(406, "text/plain")
        self.wfile.write(bytes(message, 'utf-8'))


def run(server_class=HTTPServer, handler_class=HTTPHandler, port=30123):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting notification collector server...')
    logging.info('Starting notification collector Server')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
