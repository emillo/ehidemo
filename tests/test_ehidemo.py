#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ehidemo
----------------------------------

Tests for `ehidemo` module.
"""

import unittest
import urllib.request
import random
import string

from multiprocessing import Process
from http.server import HTTPServer

from ehidemo import ehidemo


class HTTPServerTestCase(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:30123/?'
        self.httpd = HTTPServer(('', 30123), ehidemo.HTTPHandler)
        self.thread = Process(target=self.httpd.handle_request)
        self.thread.start()

    def test_happy_path(self):
        url = self.url + 'label=Los%20Angeles&payload=1234567890'
        result = urllib.request.urlopen(url).read()
        assert result == b'{"status": "ok", "notification":\
 "notification success for customer 1"}'

    def test_missing_label_raises_httperror(self):
        url = self.url + 'payload=1234567890'
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(url)

    def test_missing_payload_raises_httperror(self):
        url = self.url + 'label=Los+Angeles'
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(url)

    def test_empty_label_raises_httperror(self):
        url = self.url + 'label=&payload=1234567890'
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(url)

    def test_empty_payload_raises_httperror(self):
        url = self.url + 'label=Los%20Angeles&payload='
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(url)

    def test_two_labels_is_ok(self):
        url = self.url + \
            'label=Los+Angeles&label=New+York&payload=1234567890'
        result = urllib.request.urlopen(url).read()
        assert result == b'{"status": "ok", "notification": \
"added stray notification"}'

    def test_two_payloads_is_ko(self):
        url = self.url + \
            'label=Los%20Angeles&payload=1234567890&payload=0987654321'
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(url)

    def test_label_not_recognized(self):
        url = self.url + \
            'label=Bologna&payload=1234567890abcd'
        with self.assertRaises(urllib.error.HTTPError):
            urllib.request.urlopen(url)

    def tearDown(self):
        self.httpd.socket.close()
        self.thread.terminate()


class DAOTestCase(unittest.TestCase):

    def setUp(self):
        self.DAO = ehidemo.DAO
        self.customers = ehidemo.DAO.customers

    def test_customer_name(self):
        assert self.customers[4].name == 'Angela Davies'
        assert self.customers[3].name == 'Lily Lee'
        assert self.customers[1].name == 'Justin Wright'

    def test_customer_label(self):
        assert self.customers[4].notification_label == 'Addis Ababa'
        assert self.customers[6].notification_label == 'Kinshasa'
        assert self.customers[0].notification_label == 'Los Angeles'

    def test_get_customer_id(self):
        assert self.DAO.get_customer_id('Los Angeles') == '1'
        assert self.DAO.get_customer_id('Abidjan') == '10'
        assert self.DAO.get_customer_id('Bangkok') == '3'

    def test_get_customer_id_insensitive(self):
        assert self.DAO.get_customer_id('lOs AnGeLeS') == '1'
        assert self.DAO.get_customer_id('AbiDJan') == '10'
        assert self.DAO.get_customer_id('baNgkOk') == '3'

    def test_get_customer_not_found(self):
        assert self.DAO.get_customer_id('Bejing') is None

    def test_truncate_payload(self):
        letters = string.ascii_lowercase
        payload = ''.join(random.choice(letters) for i in range(890))
        assert len(self.DAO.truncate_payload(payload)) == 300
