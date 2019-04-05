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
        sql = 'SELECT id, email, password, phone, clinic_id, role,' \
              ' created_at,' \
              ' job, the_name AS user_name FROM users ' \
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

    def check_if_main_doctor(self, doctor_id):
        sql = 'SELECT * FROM app_pref ' \
              'WHERE main_doctor_id ='+"\"%s\"" % doctor_id.strip()
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user)

    def check_if_staff_name_exist(self, staff_name):
        sql = 'SELECT * FROM users ' \
              'WHERE the_name = "%s" AND status != 0 ' % staff_name.strip()
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user)

    def check_if_other_staff_name_exist(self, staff_name, staff_id):
        sql = 'SELECT * FROM users ' \
              'WHERE the_name = "%s" AND status != 0 AND id != "%s"' % (staff_name.strip(), staff_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user)

    def get_preferences(self, user_id):
        the_pref = ''
        sql = 'SELECT * FROM app_pref ' \
              'WHERE user_id ='+"\"%s\"" % str(user_id)
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
        else:
            sql = 'SELECT * FROM app_pref WHERE user_id = 0'
            conn = self.conn
            connection = conn.cursor()
            try:
                connection.execute(sql)
                the_pref = connection.fetchone()
            except sqlite3.OperationalError as error:
                return error
            connection.close()
            return the_pref

    def check_if_patient_name_exist(self, patient_name):
        if len(patient_name.strip()) == 0:
            return False, ''
        sql = 'SELECT * FROM patients JOIN patients_visits on'\
              ' patients_visits.id = ( select id from patients_visits' \
              ' where patients_visits.patient_id = patients.id AND patients_visits.status != 0' \
              ' AND patients_visits.clinic_id = "%s")' \
              ' WHERE patients.status != 0'\
              ' AND patient_name = "%s"' % (str(SessionWrapper.clinic_id), patient_name.strip())
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user), the_user

    def check_if_other_patient_name_exist(self, patient_name, patient_id):
        sql = 'SELECT * FROM patients JOIN patients_visits on'\
              ' patients_visits.id = ( select id from patients_visits' \
              ' where patients_visits.patient_id = patients.id AND patients_visits.status != 0' \
              ' AND patients_visits.clinic_id = "%s")' \
              ' WHERE patients.status != 0 AND patient_name = "%s" AND patients.id != "%s"' % (str(SessionWrapper.clinic_id), patient_name.strip(), patient_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user), the_user

    def check_if_patient_phone_exist(self, patient_phone):
        if len(patient_phone.strip()) == 0:
            return False, ''
        sql = 'SELECT * FROM patients JOIN patients_visits on'\
              ' patients_visits.id = ( select id from patients_visits' \
              ' where patients_visits.patient_id = patients.id AND patients_visits.status != 0' \
              ' AND patients_visits.clinic_id = "%s")' \
              ' WHERE patients.status != 0'\
              ' AND patients.phone = "%s"' % (str(SessionWrapper.clinic_id), patient_phone.strip())
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user), the_user

    def check_if_other_patient_phone_exist(self, patient_phone, patient_id):
        sql = 'SELECT * FROM patients JOIN patients_visits on'\
              ' patients_visits.id = ( select id from patients_visits' \
              ' where patients_visits.patient_id = patients.id AND patients_visits.status != 0' \
              ' AND patients_visits.clinic_id = "%s")' \
              ' WHERE patients.status != 0 AND phone = "%s" AND patients.id != "%s"' % (str(SessionWrapper.clinic_id), patient_phone.strip(), patient_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user), the_user

    def check_if_staff_phone_exist(self, staff_phone):
        sql = 'SELECT * FROM users ' \
              'WHERE phone = "%s" AND status != 0' % staff_phone.strip()
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user)

    def check_if_other_staff_phone_exist(self, staff_phone, staff_id):
        sql = 'SELECT * FROM users ' \
              'WHERE phone = "%s" AND status != 0 AND id != "%s"' % (staff_phone.strip(), staff_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user)

    def check_if_other_staff_email_exist(self, staff_email, staff_id):
        sql = 'SELECT * FROM users ' \
              'WHERE email = "%s" AND status != 0 AND id != "%s"' % (staff_email.strip(), staff_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_user = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_user)

    def check_if_prescription_option_exist(self, name, clinic_id):
        sql = 'SELECT * FROM prescription_options ' \
              'WHERE status != 0 AND medicine_name ="%s" AND clinic_id ="%s"' % (name.strip(), clinic_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_check = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_check)

    def is_doctor(self, clinic_id, staff_id):
        sql = 'SELECT * FROM users ' \
              'WHERE status != 0 AND job =1 AND id = "%s" AND clinic_id ="%s"' % (staff_id, clinic_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_check = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return bool(the_check)

    def get_clinic_info(self, clinic_id):
        query = "select clinics.*, " \
                "(SELECT COUNT(*) FROM users emp WHERE emp.clinic_id = clinics.id" \
                " AND emp.status != 0" \
                ") AS emp_count " \
                " from clinics WHERE id = " + str(clinic_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            clinic_info = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return clinic_info

    def count_clinic_doctors(self, clinic_id):
        query = "SELECT COUNT(*) emp_count FROM users " \
                " WHERE job = 1" \
                " AND status != 0" \
                " AND clinic_id = " + str(clinic_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            clinic_info = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return clinic_info['emp_count']

    def count_patient_visit(self, patient_id):
        query = "SELECT COUNT(*) visits_count FROM patients_visits " \
                " WHERE status != 0" \
                " AND patient_id = " + str(patient_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            patient_info = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return patient_info['visits_count']

    def count_patients_table(self):
        query = "SELECT patients.id"\
        " FROM patients JOIN patients_visits on"\
        " patients_visits.id = ( select id from patients_visits" \
        " where patients_visits.patient_id = patients.id AND patients_visits.status != 0" \
        " AND patients_visits.clinic_id = '%s' order by datetime(visit_time) desc limit 1)" \
        " JOIN users on users.id = patients_visits.doctor_id" \
        " WHERE patients.status != 0" % SessionWrapper.clinic_id
        last_part = " GROUP BY patients.id"
        query += last_part
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_count = connection.fetchall()
            connection.close()
            return len(the_count)
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def count_main_grid(self, clinic_id, **kwargs):
        clinic_id = str(clinic_id)
        query = "SELECT patients.id"\
        " FROM patients JOIN patients_visits on"\
        " patients_visits.id = ( select id from patients_visits" \
        " where patients_visits.patient_id = patients.id AND patients_visits.status != 0" \
        " AND patients_visits.clinic_id = '%s' order by datetime(visit_time) desc limit 1)" \
        " JOIN users on users.id = patients_visits.doctor_id" \
        " WHERE patients.status != 0" \
        " AND patients.clinic_id = '%s'"  % (clinic_id, clinic_id)

        if "doctor_filter" in kwargs:
            doctor_filter = kwargs["doctor_filter"]
            query += " AND users.the_name = '" + doctor_filter + "' "

        if "status_filter" in kwargs:
            status_filter = kwargs["status_filter"]
            good_status = status_filter[2:]
            query += " AND patients_visits.visit_status = '" + good_status + "' "

        if "date_filter" in kwargs:
            date_filter = kwargs["date_filter"]
            query += " AND patients_visits.visit_date = '" + date_filter + "' "

        if "plain_search" in kwargs:
            plain_search = kwargs["plain_search"]
            query += " AND patients.patient_name LIKE '%" + plain_search.strip() + "%' "

        last_part = " GROUP BY patients.id"
        query += last_part
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_count = connection.fetchall()
            connection.close()
            return len(the_count)
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_for_grid(self, clinic_id, page=1, per_page=10, **kwargs):
        clinic_id = str(clinic_id)
        query = "SELECT " \
        "patients.patient_name, " \
        "patients.birth_date, " \
        "patients.phone, " \
        "(SELECT COUNT(*) FROM patients_visits subp WHERE subp.patient_id = patients.id" \
        " AND subp.status != 0" \
        " AND subp.clinic_id = '" + clinic_id + "' " \
        ") AS visit_count, " \
        "patients_visits.visit_date, " \
        "patients_visits.visit_time, " \
        "users.the_name AS doctor_name, " \
        "patients_visits.visit_status, " \
        "patients_visits.id as visit_id, " \
        "datetime(patients_visits.visit_time) as date_to_order, " \
        "patients.id as patient_id " \
        "FROM patients " \
        "JOIN patients_visits " \
        "on patients_visits.id = ( " \
        "select id from patients_visits " \
        "where patients_visits.patient_id = patients.id " \
        "AND patients_visits.status != 0 " \
        "AND patients_visits.clinic_id = '" + clinic_id + "' " \
        "order by datetime(visit_time) desc limit 1) " \
        "JOIN users " \
        "on users.id = patients_visits.doctor_id " \
        "WHERE patients.status != 0 " \
        "AND patients.clinic_id = '" + clinic_id + "' "

        if "doctor_filter" in kwargs:
            doctor_filter = kwargs["doctor_filter"]
            query += " AND users.the_name = '" + doctor_filter + "' "

        if "status_filter" in kwargs:
            status_filter = kwargs["status_filter"]
            good_status = status_filter[2:]
            query += " AND patients_visits.visit_status = '" + good_status + "' "

        if "date_filter" in kwargs:
            date_filter = kwargs["date_filter"]
            query += " AND patients_visits.visit_date = '" + date_filter + "' "

        if "plain_search" in kwargs:
            plain_search = kwargs["plain_search"]
            query += " AND patients.patient_name LIKE '%" + plain_search.strip() + "%' "

        order_part = " ORDER BY date_to_order DESC"
        query += order_part

        offset = (page - 1) * per_page
        total = self.count_main_grid(clinic_id, **kwargs)
        if offset > total:
            offset = total

        total_pages = math.ceil(total/per_page)

        pagination_part = ' LIMIT %s OFFSET %s' % (per_page, offset)

        query += pagination_part
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            all_rows = connection.fetchall()
            connection.close()
            return all_rows, total_pages, total
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def count_staff_rows(self, clinic_id, search):
        search = search.strip()
        clinic_id = str(clinic_id)
        query = "SELECT count(*) " \
                "FROM users " \
                "WHERE status != 0 " \
                "AND clinic_id = '%s'" % clinic_id
        if len(search) > 0:
            query += " AND the_name LIKE '%" + search + "%' "
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_count = connection.fetchone()
            connection.close()
            return the_count[0]
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_all_staff(self, clinic_id, page=1, per_page=10, search=""):
        search = search.strip()
        clinic_id = str(clinic_id)
        query = "SELECT the_name, job, phone, role, created_at, id " \
        "FROM users " \
        "WHERE status != 0 " \
        "AND clinic_id = '%s'" % clinic_id

        if len(search) > 0:
            query += " AND the_name LIKE '%" + search + "%' "

        query += " order by datetime(created_at) desc"
        offset = (page - 1) * per_page
        total = self.count_staff_rows(clinic_id, search)
        total_users = total
        if offset > total:
            offset = total
        query += ' LIMIT %s OFFSET %s' % (per_page, offset)
        total_pages = math.ceil(total/per_page)
        # query += searchF + doctorF + statusF + " order by date_to_order DESC"

        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            all_rows = connection.fetchall()
            connection.close()
            return all_rows, total_pages, total_users
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_staff_by_id(self, staff_id):
        staff_id = str(staff_id)
        query = "SELECT the_name, job, phone, role, specialization, created_at, id " \
        "FROM users " \
        "WHERE status != 0 " \
        "AND id = '%s'" % staff_id
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_staff = connection.fetchone()
            connection.close()
            return the_staff
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def read_app_settings(self):
        query = "SELECT * FROM app_settings "
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_settings = connection.fetchone()
            connection.close()
            return the_settings
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def is_trial(self):
        query = "SELECT * FROM app_settings "
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_settings = connection.fetchone()
            connection.close()
            check = int(the_settings['field1'])
            if check == 1:
                return True
            return False
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def count_staff_visits(self, staff_id):
        staff_id = str(staff_id)
        query = "SELECT count(patients_visits.id) as staff_visits " \
        "FROM patients_visits " \
        "JOIN patients on patients.id = patients_visits.patient_id "\
        "WHERE patients_visits.status != 0 " \
        "AND patients.status != 0 " \
        "AND patients_visits.doctor_id = '%s'" % staff_id
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_staff = connection.fetchone()
            connection.close()
            return the_staff['staff_visits']
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def delete_staff(self, staff_id):
        staff_id = str(staff_id)
        query = "UPDATE users " \
                "SET status = 0 " \
                "WHERE id = '%s'" % staff_id
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            conn.commit()
            connection.close()
        except sqlite3.OperationalError as error:
            connection.close()
            return error
        return "deleted"

    # "(users.firstname || \" \" || users.lastname) AS doctor_name, " \ #
    def get_visits_for_clinic_report(self, clinic_id, start_date, end_date):
        sql2 = 'SELECT patients_visits.*, ' \
               "users.the_name AS doctor_name " \
               'FROM patients_visits ' \
               'JOIN users ' \
               'on users.id = patients_visits.doctor_id ' \
               'WHERE patients_visits.status != 0 '\
               'AND users.status != 0 '\
               'AND patients_visits.clinic_id = %s AND patients_visits.status = 1 ' \
               'AND patients_visits.visit_date >= date("%s") AND visit_date <= date("%s")' % (clinic_id, start_date, end_date)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql2)
            the_row = connection.fetchall()
            connection.close()
            return the_row
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_patient_and_visit(self, visit_id):
        sql = 'SELECT ' \
              'patients.*, '\
              'patients_visits.diagnosis, ' \
              'patients_visits.recommendations, ' \
              'patients_visits.prescription, ' \
              'patients_visits.visit_date, ' \
              'patients_visits.visit_time, ' \
              'patients_visits.visit_status, ' \
              'patients_visits.symptoms, ' \
              "users.the_name AS doctor_name, " \
              "users.specialization AS doctor_specialization, " \
              'patients_visits.id, ' \
              'patients_visits.patient_id ' \
              'FROM patients_visits ' \
              'JOIN patients ' \
              'on patients.id = patients_visits.patient_id ' \
              'JOIN users ' \
              'on users.id = patients_visits.doctor_id ' \
              'WHERE patients_visits.id = ' + str(visit_id) + ' ' \
              'AND patients_visits.status != 0 '
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_row = connection.fetchone()
            connection.close()
            return the_row
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_patient_by_id(self, patient_id):
        sql = 'SELECT * FROM patients WHERE id = ' + str(patient_id) + ' AND status != 0 '
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_row = connection.fetchone()
            connection.close()
            return the_row
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_patient_last_visit(self, patient_id):
        sql = 'SELECT ' \
              'id ' \
              'FROM patients_visits ' \
              'WHERE patient_id = ' + str(patient_id) + ' ' \
              'AND status != 0 '\
              'order by datetime(visit_time) desc limit 1'
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_row = connection.fetchone()
            connection.close()
            return the_row
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_prescription_options(self, clinic_id):
        sql = 'SELECT ' \
              'medicine_name ' \
              'FROM prescription_options ' \
              'WHERE clinic_id = ' + str(clinic_id) + ' ' \
              'AND status != 0 '\
              'order by medicine_name'
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            options = []
            for row in connection.fetchall():
                options.append(row['medicine_name'])
            connection.close()
            return options
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def count_other_visit(self, patient_id):
        patient_id = str(patient_id)
        query = 'SELECT ' \
                'patients_visits.id ' \
                'FROM patients_visits ' \
                'JOIN users ' \
                'on users.id = patients_visits.doctor_id ' \
                'WHERE patients_visits.patient_id = '+str(patient_id)+' '\
                'AND patients_visits.status != 0 '
        last_part = ' GROUP BY patients_visits.id'
        query += last_part
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            the_count = connection.fetchall()
            connection.close()
            return len(the_count)
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_other_visits(self, patient_id, page=1, per_page=5):
        sql = 'SELECT ' \
              'patients_visits.symptoms, ' \
              'patients_visits.diagnosis, ' \
              'patients_visits.recommendations, ' \
              'patients_visits.visit_date, ' \
              'users.the_name as doctor_name, ' \
              'patients_visits.visit_status, ' \
              'patients_visits.id ' \
              'FROM patients_visits ' \
              'JOIN users ' \
              'on users.id = patients_visits.doctor_id ' \
              'WHERE patients_visits.patient_id = '+str(patient_id)+' '\
              'AND patients_visits.status != 0 '\
              'order by datetime(visit_date) desc'
        offset = (page - 1) * per_page
        total = self.count_other_visit(patient_id)
        if offset > total:
            offset = total
        total_pages = math.ceil(total / per_page)
        pagination_part = ' LIMIT %s OFFSET %s' % (per_page, offset)
        sql += pagination_part
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchall()
            connection.close()
            return all_rows, total_pages
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_patient_visits_for_report(self, patient_id):
        sql = 'SELECT ' \
              'patients_visits.symptoms, ' \
              'patients_visits.diagnosis, ' \
              'patients_visits.recommendations, ' \
              'patients_visits.visit_date, ' \
              'patients_visits.visit_time, ' \
              'patients_visits.prescription, ' \
              'users.the_name as doctor_name, ' \
              'patients_visits.visit_status, ' \
              'patients_visits.id ' \
              'FROM patients_visits ' \
              'JOIN users ' \
              'on users.id = patients_visits.doctor_id ' \
              'WHERE patients_visits.patient_id = '+str(patient_id)+' '\
              'AND patients_visits.status != 0 '\
              'order by datetime(visit_date) desc'
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchall()
            connection.close()
            return all_rows
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_doctor_schedule(self, doctor_id, the_date):
        sql = 'SELECT ' \
              'patients_visits.visit_time, ' \
              'patients.patient_name ' \
              'FROM patients_visits ' \
              'JOIN users ' \
              'on users.id = patients_visits.doctor_id ' \
              'JOIN patients ' \
              'on patients.id = patients_visits.patient_id ' \
              'WHERE users.id = '+str(doctor_id)+' '\
              'AND patients_visits.visit_date = "'+str(the_date)+'" '\
              'AND patients_visits.status != 0 '\
              'order by datetime(visit_time) desc'
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchall()
            connection.close()
            return all_rows
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_all_doctors(self, clinic_id):
        query = "SELECT the_name AS doctor_name FROM users WHERE status != 0 AND job = 1 AND clinic_id = '" + str(clinic_id) + "' "
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            all_rows = connection.fetchall()
            connection.close()
            return all_rows
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_patient_info(self, patient_id):
        sql = 'SELECT ' \
              'patients.patient_name, ' \
              'patients.phone, ' \
              'patients.birth_date, ' \
              'patients.about, ' \
              'patients.id ' \
              'FROM patients ' \
              'where patients.id = '+str(patient_id)+' '\
              'AND patients.status != 0 '\

        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchone()
            connection.close()
            return all_rows
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_visit_info(self, patient_id, visit_id):
        sql = 'SELECT ' \
              'patients_visits.diagnosis, ' \
              'patients_visits.recommendations, ' \
              'patients_visits.visit_date, ' \
              'doctors.doctor_name, ' \
              'patients_visits.visit_status, ' \
              'patients_visits.time, ' \
              'patients_visits.symptoms ' \
              'FROM patients_visits ' \
              'JOIN doctors ' \
              'on doctors.id = patients_visits.doctor_id ' \
              'WHERE patients_visits.patient_id = ' + str(patient_id) + ' ' \
              'AND patients_visits.id = ' + str(visit_id)+' '\
              'AND patients_visits.status != 0'

        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchone()
            connection.close()
            return all_rows
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def select_fields(self, table_name, fields):
        i = 0
        sql = 'SELECT '
        for field in fields:
            if i == 0:
                sql += field
            else:
                sql += ', ' + field
            i += 1
        sql += ' FROM ' + table_name
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return all_rows

    def get_headers(self, table_names):
        headers = []
        conn = self.conn
        connection = conn
        for table_name in table_names:
            sql = 'PRAGMA table_info('+table_name+')'
            try:
                all_rows = conn.execute(sql).fetchall()
                for row in all_rows:
                    if row[2] in self.acceptable_types:
                        sub_row = {'name': row[1], 'data_type': row[2]}
                        headers.append(sub_row)
            except sqlite3.OperationalError as error:
                connection.close()
                return error
        return headers

    def select_where(self, table_name, arg):
        i = 0
        sql = 'SELECT * FROM '+table_name
        for col, value in arg.items():
            if i == 0:
                sql += ' WHERE '+col+'='+"\"%s\"" % value
            else:
                sql += ' AND '+col+'='+"\"%s\"" % value
            i += 1
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            all_rows = connection.fetchall()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return all_rows

    def delete_patient(self, patient_id):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE patients SET status = ? WHERE id= ? ",  (0, patient_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'Patient deleted successfully'

    def delete_patient_visit(self, visit_id):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE patients_visits SET status = ? WHERE id= ? ",  (0, visit_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'visit deleted successfully'

    def update_my_info(self, user_id, name, email, phone):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE users SET the_name = ?, email= ?, phone= ? WHERE id= ? ",  (name, email, phone, user_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'visit deleted successfully'

    def update_clinic_info(self, clinic_id, name, specialization, address, phone):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE clinics SET clinic_name = ?, specialization= ?, address= ?, phone= ? WHERE id= ? ",  (name, specialization, address, phone, clinic_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'visit deleted successfully'

    def update_my_pwd(self, user_id, pwd):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE users SET password = ? WHERE id= ? ",  (pwd, user_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'visit deleted successfully'

    def update_patient_info(self, patient_id, name, phone, birth, about):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute("UPDATE patients SET patient_name = ?, phone = ?, birth_date = ?, about = ? WHERE id= ? ",  (name, phone, birth, about, patient_id))
            conn.commit()
        except sqlite3.OperationalError as error:
            return 'Red', error
        connection.close()
        return 'Green', 'Document Updated successfully'

    def create_table(self, tbl_name, fields, foreign_keys=None):
        sql = 'CREATE TABLE '+tbl_name+' (id INTEGER NOT NULL PRIMARY KEY ASC '
        for field in fields:
            sql += ', ' + field['name'] + ' ' + field['data_type']
        if foreign_keys is not None:
            for f_key in foreign_keys:
                sql += ', FOREIGN KEY(' + f_key['field'] + ') REFERENCES '+f_key['target']+'('+f_key['target_field']+')'
        sql += ')'
        connection = self.conn
        try:
            connection.execute(sql)
            connection.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'Table Created successfully'

    def alter_table(self, tbl_name, fields):
        connection = self.conn
        sql = "ALTER TABLE "+tbl_name+" ADD COLUMN "
        i = 0
        for field in fields:
            if i == 0:
                sql += field['name'] + ' ' + field['data_type']
            else:
                sql += ', ' + field['name'] + ' ' + field['data_type']

            i += 1
        connection.execute(sql)
        connection.commit()
        return 'Done'

    def alter_foreign_key(self, tbl_name, foreign_key):
        connection = self.conn
        sql = "ALTER TABLE " + tbl_name + " CONSTRAINT fk_"+tbl_name+"_"+foreign_key['target']+" FOREIGN KEY( "  + foreign_key['field'] + ") REFERENCES "+foreign_key['target']+" ("+foreign_key['target_field']+" )"

        try:
            connection.execute(sql)
            connection.commit()
        except sqlite3.OperationalError as error:
            return error
        connection.close()
        return 'foreign key added successfully'

    def sign_up(self, the_name, email, password, roles):
        connection = self.conn
        try:
            connection.execute("INSERT INTO users (the_name, email, password, roles) VALUES (?, ?, ?, ?)", (the_name, email, password, roles))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'user added successfully'

    def insert_staff(self, clinic_id, name, phone, job, role, specialization, created_at):
        connection = self.conn
        try:
            connection.execute("INSERT INTO users (the_name, phone, clinic_id, job, role, specialization, created_at)"
                               " VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (name, phone, clinic_id, job, role, specialization, created_at))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'user added successfully'

    def update_staff(self, staff_id, name, phone, role):
        connection = self.conn
        try:
            connection.execute("UPDATE users SET the_name = ?, phone= ?, role= ? WHERE id= ?",
                               (name, phone, role, staff_id))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'user updated successfully'

    def update_remember_me(self, user_name="", pass_word=""):
        connection = self.conn
        try:
            connection.execute("UPDATE remember_me SET user_name = ?, pass_word= ? WHERE id= ?",
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

    def update_trial_time(self, the_date):
        connection = self.conn
        try:
            connection.execute("UPDATE app_settings SET field2 = ? WHERE id= ?",
                               (the_date, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'settings updated successfully'

    def update_code_origin(self, the_code):
        connection = self.conn
        try:
            connection.execute("UPDATE app_settings SET field7 = ?, field9 = 1 WHERE id= ?",
                               (the_code, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'settings updated successfully'

    def make_subscription(self, the_code, the_date):
        connection = self.conn
        try:
            connection.execute("UPDATE app_settings SET field8 = ?, field9 = 0, field1 = 0, field3 = ? WHERE id= ?",
                               (the_code, the_date, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'settings updated successfully'

    def update_paid_time(self, the_date):
        connection = self.conn
        try:
            connection.execute("UPDATE app_settings SET field3 = ? WHERE id= ?",
                               (the_date, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'settings updated successfully'

    def update_pc_id(self, pc_id):
        connection = self.conn
        try:
            connection.execute("UPDATE app_settings SET field5 = ?, field10 = 1 WHERE id= ?",
                               (pc_id, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return 'settings updated successfully'

    def insert_patient_and_visit(self, clinic_id, name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time):
        connection = self.conn
        cr = connection.cursor()
        try:
            cr.execute("INSERT INTO patients (patient_name , phone, gender, occupation, tall, weight, birth_date , about , clinic_id )"
                               " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (name, phone, gender, occupation, weight, tall, birth_date, about, clinic_id))
            connection.commit()
            patient_id = cr.lastrowid
            visit_id = self.insert_visit(patient_id, visit_date, doctor,  visit_time, clinic_id)
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error
        connection.close()
        return visit_id

    def insert_visit(self, patient_id, visit_date, doctor, visit_time, clinic_id, symptoms=""):
        doctor_id = self.get_doctor_id(doctor)
        full_time = visit_date+" "+visit_time
        visit_time = datetime.datetime.strptime(full_time, "%Y-%m-%d %H:%M:%S")
        connection = self.conn
        cr = connection.cursor()
        try:
            cr.execute(
                "INSERT INTO patients_visits (patient_id, visit_date, doctor_id, visit_status, visit_time, clinic_id, symptoms)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)", (patient_id, visit_date, doctor_id, "مجدولة", visit_time, clinic_id, symptoms))
            connection.commit()
            visit_id = cr.lastrowid
            return visit_id
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'

    def insert_prescription_option(self, medicine_name, created_by, created_at, clinic_id):
        connection = self.conn
        cr = connection.cursor()
        try:
            cr.execute(
                "INSERT INTO prescription_options (medicine_name, created_by, created_at, clinic_id, status)"
                " VALUES (?, ?, ?, ?, ?)", (medicine_name, created_by, created_at, clinic_id, 1))
            connection.commit()
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'

    def delete_prescription_option(self, medicine_name, clinic_id):
        clinic_id = str(clinic_id)
        query = "UPDATE prescription_options " \
                "SET status = 0 " \
                "WHERE clinic_id = '%s' AND medicine_name = '%s'" % (clinic_id, medicine_name)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(query)
            conn.commit()
            connection.close()
        except sqlite3.OperationalError as error:
            connection.close()
            return error
        return "deleted"

    def get_doctor_id(self, doctor_name):
        sql = 'SELECT id FROM users where the_name = \"%s\"' % doctor_name
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_doctor = connection.fetchone()
            connection.close()
            if bool(the_doctor):
                return the_doctor["id"]
            else:
                return 0
        except sqlite3.OperationalError as error:
            connection.close()
            return 0

    def get_user_name_by_id(self, doctor_id):
        sql = 'SELECT the_name FROM users where id = \"%s\"' % doctor_id
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_doctor = connection.fetchone()
            connection.close()
            if bool(the_doctor):
                return the_doctor["the_name"]
            else:
                return 0
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def get_default_doctor(self, clinic_id):
        sql = "SELECT the_name FROM users WHERE status != 0 AND job = 1 AND clinic_id = '" + str(clinic_id) + "' "
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_doctor = connection.fetchone()
            connection.close()
            if bool(the_doctor):
                return the_doctor["the_name"]
            else:
                return 0
        except sqlite3.OperationalError as error:
            connection.close()
            return error

    def update_only_patient(self, patient_id, name, birth_date, gender, occupation, weight, height, phone, about):
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(
                "UPDATE patients SET patient_name = ?, tall = ?, weight = ?, phone = ?, birth_date = ?, gender= ?, occupation= ?, about = ? WHERE id= ? ",
                (name, height, weight, phone, birth_date, gender, occupation, about, patient_id)
            )
            conn.commit()
            connection.close()
            return "Done for patient", ''
        except sqlite3.OperationalError as error:
            connection.close()
            return 'Red', error

    def update_visit(self, visit_id, doctor, visit_date, visit_time, visit_status, symptoms, diagnosis, prescription, recommendation):
        doctor_id = self.get_doctor_id(doctor)
        full_time = visit_date+" "+visit_time
        visit_time = datetime.datetime.strptime(full_time, "%Y-%m-%d %H:%M:%S")
        connection = self.conn
        cr = connection.cursor()
        try:
            cr.execute(
                "UPDATE patients_visits SET diagnosis = ?, recommendations = ?, prescription = ?, visit_date = ?, doctor_id = ?, symptoms= ?, visit_status = ?, visit_time = ? WHERE id= ?"
                , (diagnosis, recommendation, prescription, visit_date, doctor_id, symptoms, visit_status, visit_time, visit_id))
            connection.commit()
            return "Done for visit"
        except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
            return error, 'Red'

    def create_or_update_preferences(self, user_id, app_mode, main_doctor_id, font_color, regular_label_size, big_label_size):
        the_pref = ''
        sql = 'SELECT * FROM app_pref ' \
              'WHERE user_id =' + "\"%s\"" % str(user_id)
        conn = self.conn
        connection = conn.cursor()
        try:
            connection.execute(sql)
            the_pref = connection.fetchone()
        except sqlite3.OperationalError as error:
            return error
        if bool(the_pref):
            try:
                connection.execute(
                    "UPDATE app_pref SET regular_size = ?, big_size = ?, font_color = ?, app_mode = ?, main_doctor_id = ? WHERE id = ? ",
                    (regular_label_size, big_label_size, font_color, app_mode, main_doctor_id, the_pref['id'])
                 )
                conn.commit()
                connection.close()
                return "okay"
            except sqlite3.OperationalError as error:
                return error
        else:
            try:
                connection.execute(
                    "INSERT INTO app_pref (regular_size, big_size, font_color, app_mode, main_doctor_id, user_id)"
                    " VALUES (?, ?, ?, ?, ?, ?)",
                    (regular_label_size, big_label_size, font_color, app_mode, main_doctor_id, user_id))
                conn.commit()
                connection.close()
                return "okay"
            except (sqlite3.OperationalError, sqlite3.IntegrityError) as error:
                return error, 'Red'

    @staticmethod
    def clean_doc_name(text, prefix, suffix):
        if isinstance(text, (list, tuple)):
            text = text[0]
        ll = len(suffix)
        if text.endswith(suffix):
            text = text[:-ll]
        ll = len(prefix)
        word = text
        if text.startswith(prefix):
            word = text[ll:]
        return word

    @staticmethod
    def remove_suffix(text, suffix):
        ll = len(suffix)
        word = text
        if text.endswith(suffix):
            word = text[:-ll]
        return word

    @staticmethod
    def remove_prefix(text, prefix):
        ll = len(prefix)
        word = text
        if text.startswith(prefix):
            word = text[ll:]
        return word

    @staticmethod
    def clean_category(text, prefix, suffix):
        ll = len(suffix)
        if text.endswith(suffix):
            text = text[:-ll]
        ll = len(prefix)
        word = text
        if text.startswith(prefix):
            word = text[ll:]
        return word
