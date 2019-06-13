#!/usr/bin/env python3
import os
import sqlite3

from src.models.MyEnc import do_encrypt


class Database:
    data_types = ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT', 'UNSIGNED BIG INT', 'INT2', 'INT8', 'CHARACTER(20)', 'VARCHAR(255)', 'VARYING CHARACTER(255)', 'NCHAR(55)', 'NATIVE CHARACTER(70)', 'NVARCHAR(100)', 'TEXT', 'CLOB', 'BLOB', 'REAL', 'DOUBLE', 'DOUBLE PRECISION', 'FLOAT', 'NUMERIC', 'DECIMAL(10, 5)', 'BOOLEAN', 'DATE', 'DATETIME']
    acceptable_types = ['INTEGER', 'VARCHAR(255)', 'DATE', 'TEXT']

    def __init__(self):
        if not os.path.exists('resources/data'):
            os.makedirs('resources/data')
        db_file = 'resources/data/app.db'
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA key='yrewyrbdffkh'")
        conn.row_factory = sqlite3.Row
        self.conn = conn

    def reset_db_to_distribute(self):
        self.recreate_tables()
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

    def recreate_tables(self):
        sql1 = """
        DROP TABLE IF EXISTS 'app_pref';
        """
        sql2 = """
        CREATE TABLE `app_pref` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`current_version`	TEXT,
	`regular_size`	INTEGER,
	`big_size`	INTEGER,
	`font_color`	TEXT,
	`release_date`	TEXT
);
        """


        sql3 = """
                        DROP TABLE IF EXISTS 'category';
                        """
        sql4 = """ 
        CREATE TABLE `category` (
	`id`	INTEGER NOT NULL,
	`cat_name`	TEXT NOT NULL,
	`desc`	TEXT,
	`user_id`	INTEGER NOT NULL,
	`created_at`	TEXT,
	`updated_at`	TEXT,
	PRIMARY KEY(`id`)
);
        """
        sql5 = """
                                DROP TABLE IF EXISTS 'docs';
                                """
        sql6 = """ 
        CREATE TABLE `docs` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`doc_name`	TEXT,
	`details`	TEXT NOT NULL,
	`doc_type`	TEXT NOT NULL,
	`category_id`	INTEGER NOT NULL,
	`created_at`	DATETIME NOT NULL,
	`updated_at`	DATETIME,
	FOREIGN KEY(`category_id`) REFERENCES `category`(`id`)
);
        """

        sql7 = """
                                        DROP TABLE IF EXISTS 'remember_me';
                                        """
        sql8 = """ 
        CREATE TABLE `remember_me` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`user_name`	varchar ( 255 ),
	`pass_word`	varchar ( 255 )
);
        """

        sql9 = """
                                                DROP TABLE IF EXISTS 'tags';
                                                """
        sql10 = """ 
        CREATE TABLE `tags` (
	`id`	INTEGER NOT NULL,
	`tag_name`	TEXT,
	`doc_id`	INTEGER,
	PRIMARY KEY(`id`),
	FOREIGN KEY(`doc_id`) REFERENCES `docs`(`id`)
);
        """

        sql11 = """
                                                                DROP TABLE IF EXISTS 'users';
                                                                """
        sql12 = """ 
        CREATE TABLE `users` (
	`id`	INTEGER NOT NULL,
	`firstname`	VARCHAR ( 255 ) NOT NULL,
	`lastname`	VARCHAR ( 255 ) NOT NULL,
	`email`	VARCHAR ( 255 ) NOT NULL UNIQUE,
	`phone`	TEXT,
	`password`	VARCHAR ( 255 ) NOT NULL,
	`created_at`	TEXT,
	`status`	INTEGER,
	PRIMARY KEY(`id`));
        """

        connection = self.conn
        for sql in (sql1, sql2, sql3, sql4, sql5, sql6, sql7, sql8, sql9, sql10, sql11, sql12):
            connection.execute(sql)
            connection.commit()


check = Database().reset_db_to_distribute()

print(check)
