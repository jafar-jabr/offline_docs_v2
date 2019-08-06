#!/usr/bin/env python3
import sqlite3
import datetime


class Database:
    data_types = ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT', 'UNSIGNED BIG INT', 'INT2', 'INT8', 'CHARACTER(20)', 'VARCHAR(255)', 'VARYING CHARACTER(255)', 'NCHAR(55)', 'NATIVE CHARACTER(70)', 'NVARCHAR(100)', 'TEXT', 'CLOB', 'BLOB', 'REAL', 'DOUBLE', 'DOUBLE PRECISION', 'FLOAT', 'NUMERIC', 'DECIMAL(10, 5)', 'BOOLEAN', 'DATE', 'DATETIME']
    acceptable_types = ['INTEGER', 'VARCHAR(255)', 'DATE', 'TEXT']

    def __init__(self):
        db_file = 'resources/data/app.db'
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        self.conn = conn

    def create_table_if_not_exist(self, table_name, create_sql):
        sql = 'SELECT * FROM %s ' % table_name
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_check = connection.fetchone()
        except sqlite3.OperationalError as error:
            connection.execute(create_sql)
            conn.commit()
        connection.close()
        return 'Okay'

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
            print(error)
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

    def get_notes_by_date(self, the_date):
        sql = 'SELECT * FROM sticky_notes ' \
              'WHERE note_date ='+"\"%s\"" % the_date
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_notes = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        if bool(the_notes):
            return the_notes
        return []

    def update_note_pos(self, note_id, the_x, the_y, current_date):
        connection = self.conn
        try:
            connection.execute("UPDATE sticky_notes SET x_pos = ?, y_pos = ?, updated_at = ? WHERE id = ?",
                               (the_x, the_y, current_date, note_id))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'note position updated successfully'

    def update_note_details(self, note_id, the_details, current_date):
        connection = self.conn
        try:
            connection.execute("UPDATE sticky_notes SET details = ?, updated_at = ? WHERE id = ?",
                               (the_details, current_date, note_id))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'note details updated successfully'

    def insert_note(self, note_date, note_details, current_date):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(
                "INSERT INTO sticky_notes(note_date, details, created_at, updated_at) VALUES (?, ?, ?, ?)",
                  (note_date, note_details, current_date, current_date))
            conn.commit()
            connection.close()
            return connection.lastrowid
        except sqlite3.OperationalError as error:
            connection.close()
            return error

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

    def get_default_cat(self, user_id):
        query = "select * from category WHERE user_id = %s ORDER BY id" % user_id
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_categories = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return the_categories

    def get_all_categories(self, user_id):
        query = "select * from category WHERE user_id = %s" % user_id
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_categories = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return the_categories

    def get_categories_where(self, user_id, search):
        search = "%" + search + "%"
        query = "select * from category WHERE user_id = %s AND cat_name LIKE '%s'" % (user_id, search)
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

    def get_docs_ids_for_category(self, category_id):
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM docs WHERE category_id= ?", (category_id,))
            all_rows = cursor.fetchall()
        except sqlite3.OperationalError as error:
            return error
        cursor.close()
        return all_rows

    def get_detailed_docs_for_category(self, category_id):
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM docs WHERE category_id= ?", (category_id,))
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

    def update_doc(self, doc_id, doc_name, details, tags_raw):
        conn = self.conn
        connection = conn.cursor()
        try:
            self.delete_tags(doc_id)
            connection.execute("UPDATE docs SET doc_name = ?, details = ? WHERE id= ? ",  (doc_name, details, doc_id))
            conn.commit()
            self.insert_tags(tags_raw, doc_id)
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Document Updated successfully'

    def update_doc_for_import(self, doc_id, details):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE docs SET details = ? WHERE id= ? ",  (details, doc_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Document Updated successfully'

    def insert_doc(self, category_id, doc_name, details, doc_type):
        connection = self.conn
        cur_date = datetime.datetime.now()
        cr = connection.cursor()
        try:
            cr.execute("INSERT INTO docs (doc_name, details, category_id, doc_type, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)", (doc_name, details, category_id, doc_type, cur_date, cur_date))
            connection.commit()
            doc_id = cr.lastrowid
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'
        return doc_id

    def get_doc_for_category_where(self, category_id, search):
        search = "%"+search+"%"
        conn = self.conn
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Distinct doc_name FROM docs LEFT JOIN tags ON tags.doc_id = docs.id WHERE (docs.category_id= ? AND docs.doc_name LIKE ?) OR (docs.category_id= ? AND tags.tag_name LIKE ?)", (category_id, search, category_id, search,))
            all_rows = cursor.fetchall()
        except sqlite3.OperationalError as error:
            return error
        cursor.close()
        return all_rows

    def delete_doc(self, doc_id):
        conn = self.conn
        connection = conn.cursor()
        try:
            self.delete_tags(doc_id)
            connection.execute("DELETE FROM docs WHERE id= ? ",  (doc_id,))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Document Deleted successfully'

    def delete_cat(self, cat_id):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("DELETE FROM category WHERE id= ? ", (cat_id,))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Category Deleted successfully'

    def delete_tags(self, doc_id):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("DELETE FROM tags WHERE doc_id= ? ", (doc_id,))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error

    def overwrite_tags(self, tags_raw, doc_id):
        self.delete_tags(doc_id)
        already_saved = {}
        connection = self.conn
        cr = connection.cursor()
        tags = tags_raw.strip()
        the_tags = tags.split(',')
        for tag in the_tags:
            tag = tag.strip()
            if len(tag) >= 1 and tag not in already_saved:
                try:
                    cr.execute("INSERT INTO tags (tag_name, doc_id) VALUES (?, ?)", (tag, doc_id))
                    connection.commit()
                    already_saved[tag] = True
                except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
                    return error, 'Red'

    def insert_tags(self, tags_raw, doc_id):
        connection = self.conn
        cr = connection.cursor()
        tags = tags_raw.strip()
        the_tags = tags.split(',')
        for tag in the_tags:
            tag = tag.strip()
            if len(tag) >= 1:
                try:
                    cr.execute("INSERT INTO tags (tag_name, doc_id) VALUES (?, ?)", (tag, doc_id))
                    connection.commit()
                except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
                    return error, 'Red'

    def insert_cat(self, cat_name, desc, user_id, current_dat):
        connection = self.conn
        cr = connection.cursor()
        try:
            cr.execute("INSERT INTO category (cat_name, desc, user_id, updated_at, created_at) VALUES (?, ?, ?, ?, ?)", (cat_name, desc, user_id, current_dat, current_dat))
            connection.commit()
            cat_id = cr.lastrowid
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'
        return cat_id

    def update_cat(self, cat_id, cat_name, desc, current_dat):
        connection = self.conn
        cr = connection.cursor()
        try:
            cr.execute("UPDATE category set cat_name = ?, desc = ?, updated_at = ? WHERE id = ?", (cat_name, desc, current_dat, cat_id))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'
        return "Done"

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
