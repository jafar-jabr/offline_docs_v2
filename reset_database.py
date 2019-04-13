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
        ten = do_encrypt('ready to go')
        self.update_setting_to_start(ten)
        self.update_app_ref()
        self.reset_clinics()
        self.reset_patient_info()
        self.reset_patients_table()
        self.reset_visits_table()
        self.reset_prescription_options()
        self.reset_users()
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

    def update_app_ref(self):
        connection = self.conn
        try:
            connection.execute("Delete from app_pref WHERE id != 1")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'

    def reset_clinics(self):
        connection = self.conn
        try:
            connection.execute("Delete from clinics WHERE id != 1")
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

    def reset_users(self):
        connection = self.conn
        try:
            connection.execute("Delete from users WHERE id != 2")
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        return 'settings updated successfully'


check = Database().reset_db_to_distribute()

print(check)
