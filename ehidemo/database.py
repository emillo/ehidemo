# -*- coding: utf-8 -*-
import sqlite3 as dbapi
from .customer import Customer


class Database:

    def __init__(self, dbfile):
        self.dbfile = dbfile

    def add_notification(self, payload, customer_id):
        if self.is_customer_count(customer_id):
            query_count = "UPDATE notification_counters SET \
            num=num+1 WHERE id_customer=? and day=date('now')"
        else:
            query_count = "INSERT INTO notification_counters \
            (id_customer, num, day) VALUES (?, 1, date('now'))"
        connection = dbapi.connect(self.dbfile)
        connection.isolation_level = None
        cur = connection.cursor()
        cur.execute("BEGIN")
        try:
            query_notif = "INSERT INTO notifications \
            (id_customer, body) VALUES (?, ?)"
            cur.execute(query_notif, (customer_id, payload))
            cur.execute(query_count, (customer_id))
            cur.execute("COMMIT")
            success = "notification success for customer " + customer_id
            return (True, success)
        except connection.Error:
            error = "ERROR: Failed db transaction!"
            cur.execute("ROLLBACK")
            return (False, error)

    def add_stray_notification(self, payload):
        with dbapi.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = "INSERT INTO notifications \
            (body) VALUES ( ?)"
            try:
                cur.execute(query, (payload,))
                result = (True, "added stray notification")
            except connection.Error:
                result = (False, "ERROR: failed db transaction!")
            return result

    def get_customers(self):
        customers = []
        with dbapi.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = "SELECT id, name, notification_label FROM customers"
        cur.execute(query)
        for id, name, label in cur:
            customers.append(Customer(id, name, label))
        return customers

    def is_customer_count(self, customer_id):
        with dbapi.connect(self.dbfile) as connection:
            cur = connection.cursor()
            query = "SELECT num FROM notification_counters \
            WHERE id_customer =? and day = date('now')"
            cur.execute(query, (customer_id))
            return True if cur.fetchone() else False
