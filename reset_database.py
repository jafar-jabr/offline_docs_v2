#!/usr/bin/env python3

import sqlite3

from src.models.MyEnc import do_encrypt


class Database:
    data_types = ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT', 'UNSIGNED BIG INT', 'INT2', 'INT8', 'CHARACTER(20)', 'VARCHAR(255)', 'VARYING CHARACTER(255)', 'NCHAR(55)', 'NATIVE CHARACTER(70)', 'NVARCHAR(100)', 'TEXT', 'CLOB', 'BLOB', 'REAL', 'DOUBLE', 'DOUBLE PRECISION', 'FLOAT', 'NUMERIC', 'DECIMAL(10, 5)', 'BOOLEAN', 'DATE', 'DATETIME']
    acceptable_types = ['INTEGER', 'VARCHAR(255)', 'DATE', 'TEXT']

    def __init__(self):
        db_file = 'resources/data/app.db'
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA key='yrewyrbdffkh'")
        conn.row_factory = sqlite3.Row
        self.conn = conn

    def reset_db_to_distribute(self):
        self.recreate_tables()
        # ten = do_encrypt('ready to go')
        ten = do_encrypt('just start')
        self.update_setting_to_start(ten)
        self.initialize_pref()
        self.reset_pharmacys()
        self.reset_patient_info()
        self.reset_patients_table()
        self.reset_visits_table()
        self.reset_prescription_options()
        self.reset_users()
        self.reset_remember_me()
        self.remove_assets('resources/assets/images/visit_images')
        self.remove_assets('resources/assets/images/profile_images')
        self.remove_assets('resources/assets/images/logo_images')
        self.remove_assets('resources/assets/images/prescription_images')
        return ten

    def update_setting_to_start(self, ten):
        connection = self.conn
        try:
            connection.execute("UPDATE app_settings SET field1 = 1, field2 = '', field3 = '', field5 = '', field7 = '', field8 = '', field10 = ? WHERE id= ?",
                               (ten, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_pharmacys(self):
        connection = self.conn
        try:
            connection.execute("Delete from pharmacys WHERE id != 1")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_patient_info(self):
        connection = self.conn
        try:
            connection.execute("Delete from patient_info WHERE id != 1")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_patients_table(self):
        connection = self.conn
        try:
            connection.execute("Delete from patients WHERE id != 79")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_visits_table(self):
        connection = self.conn
        try:
            connection.execute("Delete from patients_visits WHERE id != 57")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_prescription_options(self):
        connection = self.conn
        try:
            connection.execute("Delete from prescription_options WHERE id Not IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_remember_me(self, user_name="", pass_word=""):
        connection = self.conn
        try:
            connection.execute("UPDATE remember_me SET user_name = ?, pass_word = ? WHERE id = ?",
                               (user_name, pass_word, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'user updated successfully'

    def reset_users(self):
        connection = self.conn
        try:
            connection.execute("Delete from users WHERE id != 2")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def recreate_tables(self):
        sql1 = """
        DROP TABLE IF EXISTS 'app_pref';
        """
        sql2 = """
        CREATE TABLE 'app_pref' (
        'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        'regular_size'	INTEGER,
        'big_size'	INTEGER,
        'font_color'	TEXT,
        'current_version'	TEXT,
        'warning_limit'	INTEGER,
        'release_date'	TEXT,
        'currency'	TEXT,
        'reports_path' TEXT);
        """

        sql3 = """
                DROP TABLE IF EXISTS 'pharmacys';
                """
        sql4 = """ 
            CREATE TABLE 'pharmacys' (
            'id'	INTEGER NOT NULL,
            'pharmacy_name'	VARCHAR(255),
            'specialization'	TEXT,
            'logo'	BLOB,
            'since'	DATE,
            'phone'	TEXT,
            'address'	TEXT,
            'updated_by'	TEXT,
            PRIMARY KEY('id')
        );
        """

        sql5 = """
                        DROP TABLE IF EXISTS 'patient_info';
                        """
        sql6 = """ 
        CREATE TABLE 'patient_info' (
            'id'	INTEGER NOT NULL,
            'patient_id'	INTEGER NOT NULL,
            'blood_group'	varchar(10),
            'marital_status'	varchar(30),
            'address'	TEXT,
            'chronic_disease'	TEXT,
            'surgery_record'	TEXT,
            'social_record'	TEXT,
            'family_record'	TEXT,
            'drug_sensitivity'	TEXT,
            'updated_by'	TEXT,
            PRIMARY KEY('id')
        );
        """
        sql7 = """
                                DROP TABLE IF EXISTS 'patients';
                                """
        sql8 = """ 
        CREATE TABLE 'patients' (
            'id'	INTEGER NOT NULL,
            'patient_name'	VARCHAR(255),
            'phone'	VARCHAR(255),
            'photo'	BLOB,
            'birth_date'	DATE,
            'tall'	INTEGER,
            'weight'	INTEGER,
            'status'	INTEGER DEFAULT 1,
            'about'	TEXT,
            'pharmacy_id'	INTEGER,
            'updated_by'	TEXT, gender varchar(100), occupation varchar(255),
            PRIMARY KEY('id')
        );
        """

        sql9 = """
                                        DROP TABLE IF EXISTS 'patients_visits';
                                        """
        sql10 = """ 
        CREATE TABLE 'patients_visits' (
            'id'	INTEGER NOT NULL,
            'patient_id'	INTEGER NOT NULL,
            'diagnosis'	TEXT,
            'recommendations'	TEXT,
            'prescription'	TEXT,
            'visit_date'	DATE,
            'doctor_id'	INTEGER,
            'symptoms'	TEXT,
            'status'	INTEGER DEFAULT 1,
            'visit_status'	VARCHAR(100),
            'visit_time'	DATETIME,
            'pharmacy_id'	INTEGER,
            'updated_by'	TEXT,
            PRIMARY KEY('id')
        );
        """

        sql11 = """
                                                DROP TABLE IF EXISTS 'prescription_options';
                                                """
        sql12 = """ 
        CREATE TABLE 'prescription_options' (
            'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            'medicine_name'	varchar(255),
            'created_by'	INTEGER,
            'created_at'	datetime,
            'pharmacy_id'	INTEGER,
            'status'	INTEGER
        );
        """

        # sql13 = """
        #                                                 DROP TABLE IF EXISTS 'remember_me';
        #                                                 """
        # sql14 = """
        # CREATE TABLE 'remember_me' (
        #     'id'	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        #     'user_name'	varchar(255),
        #     'pass_word'	varchar(255)
        # );
        # """

        sql13 = """
                                                                DROP TABLE IF EXISTS 'users';
                                                                """
        sql14 = """ 
        CREATE TABLE 'users' (
            'id'	INTEGER NOT NULL,
            'the_name'	VARCHAR(255) NOT NULL,
            'email'	VARCHAR(255) UNIQUE,
            'password'	VARCHAR(255),
            'role'	INTEGER NOT NULL,
            'pharmacy_id'	INTEGER,
            'job'	INTEGER,
            'created_at'	TEXT,
            'status'	INTEGER DEFAULT 1,
            'phone'	TEXT,
            'photo'	BLOB,
            'specialization'	TEXT,
            'updated_by'	INTEGER,
            PRIMARY KEY('id')
        );
        """
        sql15 = """
        CREATE UNIQUE INDEX UNIQ_1483A5E9E7927C74 ON users (email)
        """

        sqlp1 = """
                                                                       DROP TABLE IF EXISTS 'clients';
                                                                       """
        sqlp2 = """ 
               CREATE TABLE "clients" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"the_name"	TEXT,
	"status"	INTEGER,
	"created_at"	TEXT
);
               """

        sqlp3 = """
                                                                               DROP TABLE IF EXISTS 'manufacturers';
                                                                               """
        sqlp4 = """ 
                 CREATE TABLE "manufacturers" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"the_name"	TEXT,
	"status"	INTEGER
);
                       """

        sqlp5 = """
                                                                                       DROP TABLE IF EXISTS 'medicine_substances';
                                                                                       """
        sqlp6 = """ 
              CREATE TABLE "medicine_substances" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"medicine_id"	INTEGER,
	"substance_id"	INTEGER,
	"percentage"	NUMERIC
);
                               """
        sqlp7 = """
                                                                                               DROP TABLE IF EXISTS 'medicines';
                                                                                               """
        sqlp8 = """ 
                   CREATE TABLE "medicines" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"commercial_name"	TEXT,
	"scientific_name"	TEXT,
	"manufacturer"	TEXT,
	"made_at"	TEXT,
	"sku"	TEXT,
	"buy_price"	TEXT,
	"sell_price"	TEXT,
	"expiration_date"	TEXT,
	"available_count"	TEXT,
	"contraindications"	TEXT,
	"qr_code"	TEXT,
	"status"	INTEGER,
	"created_at"	TEXT,
	"updated_at"	TEXT
);
                                       """

        sqlp9 = """
                                                                                                       DROP TABLE IF EXISTS 'sells';
                                                                                                       """
        sqlp10 = """ CREATE TABLE "sells" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"client_name"	TEXT,
	"number_of_items"	INTEGER,
	"total_amount"	TEXT,
	"is_paid"	INTEGER,
	"created_at"	INTEGER
);
                                               """

        sqlp11 = """
                                                                                                               DROP TABLE IF EXISTS 'sold_medicines';
                                                                                                               """
        sqlp12 = """ CREATE TABLE "sold_medicines" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"sells_id"	INTEGER,
	"medicine_id"	INTEGER,
	"sold_number"	INTEGER,
	"item_price"	TEXT
);
                                                       """

        sqlp13 = """
                                                                                                                       DROP TABLE IF EXISTS 'substances';
                                                                                                                       """
        sqlp14 = """CREATE TABLE "substances" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"the_name"	TEXT,
	"status"	INTEGER
);
"""
        connection = self.conn
        for sql in (sql1, sql2, sql3, sql4, sql5, sql6, sql7, sql8, sql9, sql10, sql11, sql12, sql13, sql14, sql15):
            connection.execute(sql)
            connection.commit()

        for sql in (sqlp1, sqlp2, sqlp3, sqlp4, sqlp5, sqlp6, sqlp7, sqlp8, sqlp9, sqlp10, sqlp11, sqlp12, sqlp13, sqlp14):
            connection.execute(sql)
            connection.commit()

    def initialize_pref(self):
        sql = """
        INSERT INTO app_pref
        (regular_size, big_size, font_color, reports_path, current_version, release_date, warning_limit, currency)
        VALUES(18, 21, '#ffffff', '', '2.0.1', '01-01-2019', 0, 'US Dollar');
        """
        connection = self.conn
        connection.execute(sql)
        connection.commit()

    @staticmethod
    def remove_assets(folder):
        import os, shutil
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


check = Database().reset_db_to_distribute()

print(check)
