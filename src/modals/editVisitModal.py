from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QGridLayout
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.PrescriptionHelper import PrescriptionHelper
from src.Elements.PrescriptionInput import PrescriptionInput
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.Elements.VisitDateWidget import VisitDateWidget
from src.Elements.filteredCompoBox import FilteredCombo
from src.Elements.shortTimeWidget import ShortTimeWidget
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.Validator import Validator


class EditVisitModal(QDialog):
    def __init__(self, parent, visit_id):
        super().__init__()
        self.u_p_layout = QVBoxLayout()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.visit_id = visit_id
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        details = Database().get_patient_and_visit(self.parent.visit_id)
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("edit_visit_modal")
        self.line_width = 555
        self.layout = QVBoxLayout()
        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(3, 4)  # column, strech setColumnStretch(2, 4) #column strech
        #
        nameLabel = RegularLabel('اسم الطبيب : ')
        nameLabel.setWidth(100)

        doctor_options = Database().select_all_doctors(self.clinic_id)
        formatted_doctors_options = SharedFunctions.format_doctors_list(doctor_options)
        doctor_select = FilteredCombo(formatted_doctors_options)
        doctor_select.setCurrentText(details["doctor_name"])

        if SessionWrapper.app_mode != 1:
            first_grid.addWidget(nameLabel, 1, 0)  # ( row, column)
            first_grid.addWidget(doctor_select, 1, 1)
            i = 1
        else:
            i = 0
        visitDatetLabel = RegularLabel('التاريخ : ')

        long_line_H = QHBoxLayout()
        long_line_H.setContentsMargins(0, 0, 0, 0)
        # long_line_H.setAlignment(Qt.AlignLeft)

        date_line_Q = QWidget()
        date_line = QHBoxLayout()
        date_line.setSpacing(5)

        visitDateEdit = VisitDateWidget(-5, 0, value=details["visit_date"])

        date_line.addWidget(visitDateEdit)

        date_line_Q.setLayout(date_line)
        # date_line_Q.setMaximumWidth(350)

        time_line_Q = QWidget()
        time_line = QHBoxLayout()
        time_line.setAlignment(Qt.AlignLeft)
        time_line.setSpacing(5)
        visitTimeLabel = RegularLabel('الوقت :')
        only_time = SharedFunctions.only_time(details["visit_time"])
        visitTimeEdit = ShortTimeWidget(value=only_time)
        time_line.addWidget(visitTimeLabel)
        time_line.addWidget(visitTimeEdit)
        time_line_Q.setLayout(time_line)
        time_line_Q.setMaximumWidth(300)

        status_line = QHBoxLayout()
        status_line.setAlignment(Qt.AlignLeft)
        status_line.setSpacing(5)
        visit_status = RegularLabel('الحالة : ')
        visit_status_options = ["مجدولة", "كاملة", "ملغية"]
        visit_status_select = FilteredCombo(visit_status_options)
        visit_status_select.setCurrentText(details["visit_status"])
        status_line.addWidget(visit_status)
        status_line.addWidget(visit_status_select)

        long_line_H.addWidget(date_line_Q)
        long_line_H.addWidget(time_line_Q)
        long_line_H.addLayout(status_line)
        long_line_H.setAlignment(Qt.AlignLeft)
        # long_line_H.setSpacing(150)
        long_line_Q = QWidget()
        long_line_Q.setLayout(long_line_H)
        long_line_Q.setFixedWidth(885)
        first_grid.addWidget(visitDatetLabel, i+1, 0)  # ( row, column)
        first_grid.addWidget(long_line_Q, i+1, 1)

        symptoms_l = RegularLabel('الاعراض : ')
        symptoms_i = RegularTextArea(int(self.pc_height * 0.11), int(self.pc_width * 0.47),
                                     text=details["symptoms"], placeHolder="استخدم الفارزة (,) للفصل بين الفقرات",
                                     spacing=20)

        first_grid.addWidget(symptoms_l, i+2, 0)  # ( row, column)
        first_grid.addWidget(symptoms_i, i+2, 1)

        diagnosis_l = RegularLabel('التشخيص :')
        diagnosis_i = RegularTextArea(int(self.pc_height * 0.11), int(self.pc_width * 0.47),
                                      text=details["diagnosis"], placeHolder="استخدم الفارزة (,) للفصل بين الفقرات",
                                      spacing=20)

        first_grid.addWidget(diagnosis_l, i+3, 0)  # ( row, column)
        first_grid.addWidget(diagnosis_i, i+3, 1)

        prescription_l = RegularLabel('الوصفة   : ')

        prescriptionH = QHBoxLayout()
        prescriptionH.setContentsMargins(0, 0, 0, 0)
        self.prescriptionQ = RegularTextArea(int(self.pc_height * 0.11), int(self.pc_width * 0.35),
                                      text=details["prescription"], placeHolder="استخدم الفارزة (,) للفصل بين الفقرات",
                                      spacing=20)

        clinic_id = SessionWrapper.clinic_id
        prescription_options = Database().get_prescription_options(clinic_id)
        self.prescription_helper = PrescriptionHelper(110, self.prescriptionQ, options=prescription_options)

        self.prescription_helper.iconClicked.connect(self.add_option)
        self.prescription_helper.listRightClicked.connect(self.delete_option)

        prescriptionH.addWidget(self.prescriptionQ)
        prescriptionH.addWidget(self.prescription_helper)
        prescription_C = QWidget()
        prescriptionH.setAlignment(Qt.AlignLeft)
        prescriptionH.setSpacing(0)
        # prescription_C.setFixedWidth(int(self.pc_width * 0.47))
        prescription_C.setContentsMargins(0, 0, 0, 0)
        prescription_C.setLayout(prescriptionH)

        first_grid.addWidget(prescription_l, i+4, 0)  # ( row, column)
        first_grid.addWidget(prescription_C, i+4, 1)

        recom_l = RegularLabel('التوصيات :')
        recom_i = RegularTextArea(int(self.pc_height * 0.11), int(self.pc_width * 0.47),
                                  text=details["recommendations"],
                                  placeHolder="استخدم الفارزة (,) للفصل بين الفقرات",
                                  spacing=20)

        first_grid.addWidget(recom_l, i+5, 0)  # ( row, column)
        first_grid.addWidget(recom_i, i+5, 1)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(40, 0, int(self.pc_width * 0.18), 20)  # (left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.setMaximumWidth(100)
        if SessionWrapper.app_mode != 1:
            saveBtn.clicked.connect(lambda: self.do_update_visit(doctor_select.currentText(),
                                                             visitDateEdit.value(), visitTimeEdit.value(),
                                                             visit_status_select.currentText(),
                                                             symptoms_i.toPlainText(),
                                                             diagnosis_i.toPlainText(),
                                                             self.prescriptionQ.toPlainText(),
                                                             recom_i.toPlainText()))
        else:
            doctor_name = SharedFunctions.get_main_doctor()
            saveBtn.clicked.connect(lambda: self.do_update_visit(doctor_name,
                                                                 visitDateEdit.value(), visitTimeEdit.value(),
                                                                 visit_status_select.currentText(),
                                                                 symptoms_i.toPlainText(),
                                                                 diagnosis_i.toPlainText(),
                                                                 self.prescriptionQ.toPlainText(),
                                                                 recom_i.toPlainText()))
        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)
        btnLineQ.setFixedWidth(int(self.pc_width * 0.5))
        self.layout.addLayout(first_grid)
        self.layout.addWidget(btnLineQ)
        self.setLayout(self.layout)
        self.setWindowTitle("تعديل بيانات الزيارة")

    def check_user(self, the_name):
        check, message = Validator().validate_name(the_name)
        if not check:
            MessageBoxes.warning_message("خطأ", message)
        else:
            name_exist, patient_data_c = Database().check_if_patient_name_exist(the_name)
            if name_exist:
                will_go = MessageBoxes.patient_exist("خطأ", "الاسم موجود مسبقاً في جدول المراجعين")
                if will_go:
                    self.go_to_patient(patient_data_c['id'])
                return
            else:
                MessageBoxes.success_message("جديد", "الاسم غير مستعمل مسبقاً")

    def go_to_patient(self, patient_id):
        last_visit_data = Database().get_patient_last_visit(patient_id)
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to("patient_details", visit_id=last_visit_data['id'])

    def do_update_visit(self, doctor, visit_date, visit_time, visit_status, symptoms, diagnosis, prescription, recommendation):
        for check, message in [Validator().validate_option(doctor, "اسم الطبيب مطلوب !"),
                               Validator().validate_date(visit_date, "تاريخ الزيارة")
                               ]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        if SharedFunctions.is_future(visit_date) and visit_status == "كاملة":
            MessageBoxes.warning_message("خطأ", "لا يمكن ان تكون حالة المراجعة كاملة قبل ان يحين موعدها")
            return
        if SharedFunctions.is_past(visit_date) and visit_status == "مجدولة":
            MessageBoxes.warning_message("خطأ", "لا يمكن ان تكون حالة المراجعة مجدولة في الماضي")
            return
        Database().update_visit(self.visit_id, doctor, visit_date, visit_time, visit_status, symptoms, diagnosis, prescription, recommendation)
        MessageBoxes.success_message("تأكيد!", "تم تحديث البيانات")
        self.accept()

    def add_option(self):
        medicine_name = self.prescription_helper.get_sub_text()
        clinic_id = SessionWrapper.clinic_id
        if len(medicine_name) > 1:
            check = Database().check_if_prescription_option_exist(medicine_name, clinic_id)
            if check:
                MessageBoxes.warning_message("خطأ", "الاسم موجود مسبقا")
                return
            created_at = SharedFunctions.get_current_date_str()
            user_id = SessionWrapper.user_id
            Database().insert_prescription_option(medicine_name, user_id, created_at, clinic_id)
            MessageBoxes.success_message("تأكيد!", "تم الحفظ")
            prescription_options = Database().get_prescription_options(clinic_id)
            self.prescription_helper.update_options(prescription_options, medicine_name)

    def delete_option(self, text):
        txt = "هل انت متأكد من رغبتك بحذف "+text+" ؟"
        confirm = MessageBoxes.confirm_message(txt)
        if confirm:
            clinic_id = SessionWrapper.clinic_id
            Database().delete_prescription_option(text, clinic_id)
            self.prescription_helper.remove_option(text)
