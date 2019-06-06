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

    def get_docs_for_category(self, category_id):
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT doc_name FROM docs WHERE category_id= ?", (category_id,))
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

    def register_user(self, first_name, last_name, email, password, created_at):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(
                "INSERT INTO users(firstname, lastname, email, password, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (first_name, last_name, email, password, 1, created_at))
            conn.commit()
            connection.close()
            return connection.lastrowid
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_doc_for_category_where(self, category, search):
        category = self.clean_category(category, "('", "',)")
        category_id = self.select_where('category', {'cat_name': category})[0][0]
        search = "%"+search+"%"
        conn = self.connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Distinct doc_name FROM docs LEFT JOIN tags ON tags.doc_id = docs.id WHERE (docs.category_id= ? AND docs.doc_name LIKE ?) OR (docs.category_id= ? AND tags.tag_name LIKE ?)", (category_id, search, category_id, search,))
            all_rows = cursor.fetchall()
        except sqlite3.OperationalError as error:
            return error
        cursor.close()
        return all_rows

    def update_doc_details(self, doc_id, details, tags_raw):
        conn = self.connect_to_db()
        connection = conn.cursor()
        try:
            self.delete_tags(doc_id)
            connection.execute("UPDATE docs SET details = ? WHERE id= ? ",  (details, doc_id))
            conn.commit()
            self.insert_tags(tags_raw, doc_id)
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Document Updated successfully'

    def delete_doc_details(self, doc_id):
        conn = self.connect_to_db()
        connection = conn.cursor()
        try:
            self.delete_tags(doc_id)
            connection.execute("DELETE FROM docs WHERE id= ? ",  (doc_id,))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Document Deleted successfully'

    def delete_tags(self, doc_id):
        conn = self.connect_to_db()
        connection = conn.cursor()
        try:
            connection.execute("DELETE FROM tags WHERE doc_id= ? ", (doc_id,))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error

    def insert_doc(self, category, doc_name, details, tags):
        category = self.clean_category(category, "('", "',)")
        connection = self.connect_to_db()
        category_id = self.select_where('category', {'cat_name': category})[0][0]
        cur_date = datetime.datetime.now()
        cr = connection.cursor()
        try:
            cr.execute("INSERT INTO docs (doc_name, details, category_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?)", (doc_name, details, category_id, cur_date, cur_date))
            connection.commit()
            doc_id = cr.lastrowid
            self.insert_tags(tags, doc_id)
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'
        return 'Doc saved successfully', 'Green'

    def insert_tags(self, tags_raw, doc_id):
        connection = self.connect_to_db()
        cr = connection.cursor()
        tags = tags_raw.strip()
        the_tags = tags.split(',')
        for tag in the_tags:
            try:
                cr.execute("INSERT INTO tags (tag_name, doc_id) VALUES (?, ?)", (tag, doc_id))
                connection.commit()
            except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
                return error, 'Red'

    def insert_cat(self, cat_name, desc):
        connection = self.connect_to_db()
        cr = connection.cursor()
        try:
            cr.execute("INSERT INTO category (cat_name, desc) VALUES (?, ?)", (cat_name, desc))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'
        return 'Category saved successfully', 'Green'
