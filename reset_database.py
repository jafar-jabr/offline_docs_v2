#!/usr/bin/env python3
import os
import sqlite3


class Database:
    def __init__(self):
        db_directory = 'resources/data'
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
        db_file = db_directory+'/app.db'
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        self.conn = conn

    def reset_db_to_distribute(self):
        self.recreate_tables("resources/database.sql")
        self.initialize_pref()
        self.reset_remember_me()
        return "reset DONE"

    def reset_remember_me(self):
        connection = self.conn
        try:
            connection.execute("INSERT INTO remember_me(user_name, pass_word) VALUES (NULL,NULL);")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'user updated successfully'

    def initialize_pref(self):
        sql = """
        INSERT INTO app_pref
        (regular_size, big_size, font_color, current_version, release_date)
        VALUES(18, 21, '#000000', 'V2.0.0', '01-01-2019');
        """
        connection = self.conn
        connection.execute(sql)
        connection.commit()

    def recreate_tables(self, sql_file):
        connection = self.conn
        fd = open(sql_file, 'r')
        sqlFile = fd.read()
        fd.close()
        sqlCommands = sqlFile.split(';')
        for command in sqlCommands:
            try:
                connection.execute(command)
                connection.commit()
            except sqlite3.OperationalError:
                print("Command skipped: ", command)


check = Database().reset_db_to_distribute()

print(check)
