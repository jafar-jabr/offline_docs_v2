#!/usr/bin/env python3
import math
import sqlite3
# from pysqlcipher3 import dbapi2 as sqlite3
import datetime

from src.models.SessionWrapper import SessionWrapper


class RemoteDatabase:
    def __init__(self, db_file):
        # db_file = 'resources/data/e_app.db'
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA key='yrewyrbdffkh'")
        conn.row_factory = sqlite3.Row
        self.conn = conn

    def get_docs_for_category(self, category_name):
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM docs join category on category.id = docs.category_id WHERE category.cat_name= ?", (category_name,))
            all_rows = cursor.fetchall()
        except sqlite3.OperationalError as error:
            return error
        cursor.close()
        return all_rows

    def get_doc_details(self, category_id, doc_name):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("SELECT * FROM docs WHERE doc_name=? AND category_id =?", (doc_name, category_id))
            all_rows = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return all_rows

    def get_tags_by_doc(self, doc_id):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("SELECT tag_name FROM tags WHERE doc_id=?", (doc_id,))
            all_rows = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return all_rows

    def get_all_tags(self):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("SELECT * FROM tags")
            all_rows = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return all_rows
