#!/usr/bin/env python3
import math
import sqlite3
# from pysqlcipher3 import dbapi2 as sqlite3
import datetime

from src.models.SessionWrapper import SessionWrapper


class Database:
    data_types = ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT', 'UNSIGNED BIG INT', 'INT2', 'INT8', 'CHARACTER(20)', 'VARCHAR(255)', 'VARYING CHARACTER(255)', 'NCHAR(55)', 'NATIVE CHARACTER(70)', 'NVARCHAR(100)', 'TEXT', 'CLOB', 'BLOB', 'REAL', 'DOUBLE', 'DOUBLE PRECISION', 'FLOAT', 'NUMERIC', 'DECIMAL(10, 5)', 'BOOLEAN', 'DATE', 'DATETIME']
    acceptable_types = ['INTEGER', 'VARCHAR(255)', 'DATE', 'TEXT']

    def __init__(self):
        db_file = 'resources/data/app.db'
        # db_file = 'resources/data/e_app.db'
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA key='yrewyrbdffkh'")
        conn.row_factory = sqlite3.Row
        self.conn = conn

    def new_check_login(self, user_name):
        sql = 'SELECT * FROM users ' \
              'WHERE status != 0 '\
              'AND (email = "%s" OR phone = "%s")' % (user_name, user_name)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return the_user

    def get_preferences(self, user_id):
        sql = 'SELECT * FROM app_pref ' \
              'WHERE id ='+"\"%s\"" % str(user_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_pref = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        if bool(the_pref):
            return the_pref
        return []

    def update_remember_me(self, user_name="", pass_word=""):
        connection = self.conn
        try:
            connection.execute("UPDATE remember_me SET user_name = ?, pass_word = ? WHERE id = ?",
                               (user_name, pass_word, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'user updated successfully'

    def get_remember_me(self):
        sql = 'SELECT * FROM remember_me where id = 1'
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_data = connection.fetchone()
            connection.close()
            return the_data
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_all_categories(self):
        query = "select * from category"
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_categories = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return the_categories
