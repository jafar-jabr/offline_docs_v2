from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QGridLayout

from src.Elements.CustomLabel import RegularLabel
from src.Elements.DateWidget import DateWidget
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.Elements.TimeWidget import TimeWidget
from src.Elements.filteredCompoBox import FilteredCombo
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.Validator import Validator


class AddAppointmentModal(QDialog):
    def __init__(self, patient_id, patient_name):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.status = "Not Done"
        self.patient_id = patient_id
        self.setLayoutDirection(Qt.RightToLeft)
        self.clinic_id = SessionWrapper.clinic_id
        self.setObjectName("add_appointment")
        self.line_width = 480
        body = QVBoxLayout()

        if SessionWrapper.app_mode == 1:
            self.setFixedHeight(350)
        else:
            self.setFixedHeight(420)
        visit_info = QHBoxLayout()
        visit_info.setContentsMargins(0, 0, 10, 0)  # (left, top, right, bottom)
        the_patient_name = RegularLabel('    اسم المراجع : '+patient_name)

        visit_info.addWidget(the_patient_name)

        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(3, 2)  # column, strech

        visitDatetLabel = RegularLabel('تاريخ المراجعة :')
        visitDateEdit = DateWidget(-5, 0)

        first_grid.addWidget(visitDatetLabel, 1, 0)  # ( row, column)
        first_grid.addWidget(visitDateEdit, 1, 1)

        visitTimeLabel = RegularLabel('الوقت :')
        visitTimeEdit = TimeWidget()

        first_grid.addWidget(visitTimeLabel, 2, 0)  # ( row, column)
        first_grid.addWidget(visitTimeEdit, 2, 1)

        if SessionWrapper.app_mode != 1:
            doctor_name_label = RegularLabel('اسم الطبيب :         ')
            doctor_options = Database().select_all_doctors(self.clinic_id)
            formatted_doctors_options = SharedFunctions.format_doctors_list(doctor_options, "اختر")
            doctor_select = FilteredCombo(formatted_doctors_options, width=230)

            first_grid.addWidget(doctor_name_label, 3, 0)  # ( row, column)
            first_grid.addWidget(doctor_select, 3, 1)
            next_i = 4
        else:
            next_i = 3

        symptomsLabel = RegularLabel('الاعراض ( اختياري ) :')
        symptomsBody = RegularTextArea(placeHolder="استخدم الفارزة (,) للفصل بين الفقرات")

        first_grid.addWidget(symptomsLabel, next_i, 0)  # ( row, column)
        first_grid.addWidget(symptomsBody, next_i, 1)

        btn_line = QHBoxLayout()
        btn_line.setContentsMargins(0, 0, 440, 0)  # (left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.setFixedWidth(100)
        if SessionWrapper.app_mode == 1:
            doctor_name = SharedFunctions.get_main_doctor()
            saveBtn.clicked.connect(lambda: self.do_appointment(visitDateEdit.value(),
                                                            visitTimeEdit.value(),
                                                            doctor_name,
                                                            symptomsBody.toPlainText()))
        else:
            saveBtn.clicked.connect(lambda: self.do_appointment(visitDateEdit.value(),
                                                                visitTimeEdit.value(),
                                                                doctor_select.currentText(),
                                                                symptomsBody.toPlainText()))
        btn_line.addWidget(saveBtn)

        body.addLayout(visit_info)
        body.addLayout(first_grid)
        body.addLayout(btn_line)
        body.setAlignment(Qt.AlignTop)
        self.resize(600, 420) #width, height
        self.setWindowTitle("اضافة موعد مراجعة")
        self.setLayout(body)

    def do_appointment(self, visit_date, visit_time, doctor, symptoms):
        for check, message in [Validator().validate_option(doctor, "اسم الطبيب مطلوب !"),
                               Validator().validate_date(visit_date, "تاريخ الزيارة", future=True)
                               ]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        Database().insert_visit(self.patient_id, visit_date, doctor, visit_time, self.clinic_id, symptoms)
        MessageBoxes.success_message("تأكيد!", "تم حفظ موعد الزيارة")
        self.status = "Done"
        self.accept()

