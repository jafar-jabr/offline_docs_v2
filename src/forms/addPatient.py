from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.CustomLabel import RegularLabel
from src.Elements.DateWidget import DateWidget
from src.Elements.IconTextBoxAR import IconTextBoxAR
from src.Elements.LikeComboBox import LikeComboBox
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.Elements.RegularTextBox import RegularTextBoxAR
from src.Elements.TimeWidget import TimeWidget
from src.Elements.VisitDateWidget import VisitDateWidget
from src.modals.doctorScheduleModal import DoctorScheduleModal
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.UserBlock import UserBlock
from src.Elements.filteredCompoBox import FilteredCombo
from src.models.Validator import Validator


class AddPatient(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.initUI()
        self.setFixedHeight(700)

    def initUI(self):
        self.line_width = int(self.pc_width * 0.3)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 20) #(left, top, right, bottom)
        UserBlock(self)
        noteLabel = RegularLabel('تأكد ان لا يكون المراجع مسجل مسبقاً في قاعدة البيانات')

        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(3, 4) #column, strech setColumnStretch(2, 4) #column strech
    #
        nameLabel = RegularLabel('اسم المراجع :')
        nameLabel.setWidth(100)
        self.nameEdit = IconTextBoxAR()
        self.nameEdit.setFixedWidth(242)
        self.nameEdit.iconClicked.connect(lambda: self.check_user(self.nameEdit.text()))
        first_grid.addWidget(nameLabel, 1, 0)  # ( row, column)
        first_grid.addWidget(self.nameEdit, 1, 1)
    #
        birthDateLabel = RegularLabel('تاريخ الميلاد :')
        birthDateLabel.setWidth(100)
        self.birthdateEdit = DateWidget(0, 100)

        genderLabel = RegularLabel('                          الجنس :')
        genderLabel.setWidth(200)
        gender_options = ["اختر", "انثى", "ذكر"]
        self.gender_select = FilteredCombo(gender_options)

        birth_gender_l = QHBoxLayout()
        birth_gender_l.addWidget(self.birthdateEdit)
        birth_gender_l.addWidget(genderLabel)
        birth_gender_l.addWidget(self.gender_select)
        birth_gender_q = QWidget()
        birth_gender_q.setFixedWidth(750)
        birth_gender_q.setLayout(birth_gender_l)

        first_grid.addWidget(birthDateLabel, 2, 0)  # ( row, column)
        first_grid.addWidget(birth_gender_q, 2, 1)

        phoneLabel = RegularLabel('رقم الهاتف ( اختياري ) :')
        phoneLabel.setWidth(100)
        self.phoneEdit = RegularTextBoxAR()
        self.phoneEdit.setFixedWidth(235)

        occupationLabel = RegularLabel('             العمل ( اختياري ) :')
        occupationLabel.setWidth(200)

        self.occupation_input = RegularTextBoxAR(240)

        phone_work_l = QHBoxLayout()
        phone_work_l.addWidget(self.phoneEdit)
        phone_work_l.addWidget(occupationLabel)
        phone_work_l.addWidget(self.occupation_input)
        phone_work_q = QWidget()
        phone_work_q.setFixedWidth(750)
        phone_work_q.setLayout(phone_work_l)

        first_grid.addWidget(phoneLabel, 3, 0)  # ( row, column)
        first_grid.addWidget(phone_work_q, 3, 1)

        tall_label = RegularLabel('الطول (اختياري) :')
        tall_label.setWidth(100)
        tall_edit_h = QHBoxLayout()
        tall_edit_h.setContentsMargins(0, 0, 0, 0)
        self.tall_edit = RegularTextBoxAR()
        self.tall_edit.setValidator(QIntValidator())
        self.tall_edit.setFixedWidth(235)
        tall_unit = RegularLabel('<i style="font-size: 14px">سم</i>')
        tall_edit_h.addWidget(self.tall_edit)
        tall_edit_h.addWidget(tall_unit)
        tall_q = QWidget()
        tall_q.setLayout(tall_edit_h)

        weight_label = RegularLabel('الوزن ( اختياري ) :')
        weight_label.setWidth(100)
        weight_edit_h = QHBoxLayout()
        weight_edit_h.setContentsMargins(0, 0, 0, 0)
        weight_edit_q = QWidget()
        self.weight_edit = RegularTextBoxAR()
        self.weight_edit.setValidator(QIntValidator())
        self.weight_edit.setFixedWidth(235)
        weight_unit = RegularLabel('<i style="font-size: 14px">كغم</i>')
        weight_edit_h.addWidget(self.weight_edit)
        weight_edit_h.addWidget(weight_unit)
        weight_edit_q.setLayout(weight_edit_h)

        height_and_wieght_l = QHBoxLayout()
        height_and_wieght_l.addWidget(tall_q)
        height_and_wieght_l.addWidget(weight_label)
        height_and_wieght_l.addWidget(weight_edit_q)
        height_and_wieght_q = QWidget()
        height_and_wieght_q.setFixedWidth(850)
        height_and_wieght_q.setLayout(height_and_wieght_l)

        first_grid.addWidget(tall_label, 4, 0)  # ( row, column)
        first_grid.addWidget(height_and_wieght_q, 4, 1)

        about_l = RegularLabel('حول ( اختياري ) :')
        about_l.setWidth(100)
        self.about_f = RegularTextArea(90, int(self.pc_width*0.5), placeHolder="معلومات تخص التاريخ المرضي للمراجع (ان وجدت)")
        first_grid.addWidget(about_l, 5, 0)  # ( row, column)
        first_grid.addWidget(self.about_f, 5, 1)

        if SessionWrapper.app_mode == 1:
            self.main_doctor_name = SharedFunctions.get_main_doctor()
            doctorLabel = RegularLabel('الطبيب :')
            doctorLabel.setWidth(200)
            self.doctor_select = LikeComboBox(self.main_doctor_name)
            doctor_schedule_label = ClickableIcon(35, 35, 'resources/assets/images/dr-calendar.png', 'معاينة جدول الطبيب')
            doctor_schedule_label.clicked.connect(lambda: self.show_doctor_schedule(self.doctor_select.currentText()))
            doctor_select_h = QHBoxLayout()
            doctor_select_h.addWidget(self.doctor_select)
            doctor_select_h.addWidget(doctor_schedule_label)
            doctor_select_q = QWidget()
            doctor_select_q.setLayout(doctor_select_h)
            doctor_select_q.setFixedWidth(300)
            first_grid.addWidget(doctorLabel, 6, 0)  # ( row, column)
            first_grid.addWidget(doctor_select_q, 6, 1)
        else:
            doctorLabel = RegularLabel('الطبيب :')
            doctorLabel.setWidth(200)
            doctor_options = Database().select_all_doctors(self.clinic_id)
            formatted_doctors_options = SharedFunctions.format_doctors_list(doctor_options, "اختر")
            self.doctor_select = FilteredCombo(formatted_doctors_options)
            doctor_schedule_label = ClickableIcon(35, 35, 'resources/assets/images/dr-calendar.png', 'معاينة جدول الطبيب')
            doctor_schedule_label.clicked.connect(lambda: self.show_doctor_schedule(self.doctor_select.currentText()))
            doctor_select_h = QHBoxLayout()
            doctor_select_h.addWidget(self.doctor_select)
            doctor_select_h.addWidget(doctor_schedule_label)
            doctor_select_q = QWidget()
            doctor_select_q.setLayout(doctor_select_h)
            doctor_select_q.setFixedWidth(300)
            first_grid.addWidget(doctorLabel, 6, 0)  # ( row, column)
            first_grid.addWidget(doctor_select_q, 6, 1)
        time_line = QHBoxLayout()
        visitDatetLabel = RegularLabel('تاريخ المراجعة :')
        visitDatetLabel.setWidth(200)
        self.visitDateEdit = VisitDateWidget(-5, 0)

        visitTimeLabel = RegularLabel('الوقت :')
        visitTimeLabel.setWidth(200)
        self.visitTimeEdit = TimeWidget()

        time_line.addWidget(self.visitDateEdit)
        time_line.addWidget(visitTimeLabel)
        time_line.addWidget(self.visitTimeEdit)
        time_line_q = QWidget()
        time_line_q.setFixedWidth(560)
        time_line_q.setLayout(time_line)
        first_grid.addWidget(visitDatetLabel, 7, 0)  # ( row, column)
        first_grid.addWidget(time_line_q, 7, 1)

        btnLine = QHBoxLayout()
        # btnLine.setContentsMargins(40, 0, int(self.pc_width*0.38), 20) #(left, top, right, bottom)
        btnLine.setContentsMargins(40, 0, 20, 20) #(left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.setMaximumWidth(100)
        saveBtn.clicked.connect(lambda: self.do_add_patient(self.nameEdit.text(), self.birthdateEdit.value(),
                                                            self.phoneEdit.text(),
                                                            self.gender_select.currentText(),
                                                            self.occupation_input.text(),
                                                            self.weight_edit.text(),
                                                            self.tall_edit.text(),
                                                            self.about_f.toPlainText(),
                                                            self.doctor_select.currentText(),
                                                            self.visitDateEdit.value(),
                                                            self.visitTimeEdit.value()))

        saveAndContinueBtn = RegularButton('حفظ و استمرار')
        saveAndContinueBtn.setMaximumWidth(150)
        saveAndContinueBtn.clicked.connect(lambda: self.do_add_patient_and_continue(self.nameEdit.text(), self.birthdateEdit.value(),
                                                                                    self.phoneEdit.text(),
                                                                                    self.gender_select.currentText(),
                                                                                    self.occupation_input.text(),
                                                                                    self.weight_edit.text(),
                                                                                    self.tall_edit.text(),
                                                                                    self.about_f.toPlainText(),
                                                                                    self.doctor_select.currentText(),
                                                                                    self.visitDateEdit.value(),
                                                                                    self.visitTimeEdit.value()))
        btnLine.addWidget(saveBtn)
        btnLine.addWidget(saveAndContinueBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)
        btnLineQ.setFixedWidth(400)
        self.layout.addWidget(noteLabel)
        self.layout.addLayout(first_grid)
        self.layout.addWidget(btnLineQ)
        self.setLayout(self.layout)

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

    def do_add_patient(self, name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time):
        check = self.check_before_save(name, birth_date, phone, gender, occupation, weight, tall, about, doctor,
                                       visit_date, visit_time)
        if check:
            Database().insert_patient_and_visit(self.clinic_id, name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time)
            MessageBoxes.success_message("تأكيد!", "تم حفظ بيانات المراجع")
            self.reset_form()

    def do_add_patient_and_continue(self, name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time):
        check = self.check_before_save(name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time)
        if check:
            visit_id = Database().insert_patient_and_visit(self.clinic_id, name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time)
            from src.models.PlayMouth import PlayMouth
            PlayMouth(self.parent).go_to("patient_details", visit_id=visit_id)

    def go_to_patient(self, patient_id):
        last_visit_data = Database().get_patient_last_visit(patient_id)
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to("patient_details", visit_id=last_visit_data['id'])

    def reset_form(self):
        self.nameEdit.setText("")
        self.phoneEdit.setText("")
        self.weight_edit.setText("")
        self.tall_edit.setText("")
        self.about_f.setPlainText("")
        self.occupation_input.setText("")
        self.gender_select.setCurrentText("اختر")
        # self.doctor_select.setCurrentText("اختر")

    def show_doctor_schedule(self, doctor_name):
        schedule_date = self.visitDateEdit.value()
        doctor_id = Database().get_doctor_id(doctor_name)
        title = "جدول "+doctor_name+" ليوم "+schedule_date
        if doctor_id > 0:
            schedule = Database().select_doctor_schedule(doctor_id, schedule_date)
            if len(schedule) > 0:
                the_text = '<div>'
                for row in schedule:
                    visit_time = SharedFunctions.readableTime(row['visit_time'])
                    the_text += '<p><b>' + visit_time+'  '+row['patient_name'] + '</b></p></br>'
                the_text += '</div>'
            else:
                the_text = 'لا يوجد اي مراجعات مقررة لهذا اليوم'
            DoctorScheduleModal(title, the_text)

    def check_before_save(self, name, birth_date, phone, gender, occupation, weight, tall, about, doctor, visit_date, visit_time):
        name_exist, patient_data_c = Database().check_if_patient_name_exist(name)
        phone_exist, patient_data_c2 = Database().check_if_patient_phone_exist(phone)
        if name_exist and len(name) > 0:
            will_go = MessageBoxes.patient_exist("خطأ", "الاسم موجود مسبقاً في جدول المراجعين")
            if will_go:
                self.go_to_patient(patient_data_c['id'])
            return False
        if phone_exist and len(phone) > 0:
            will_go = MessageBoxes.patient_exist("خطأ", "رقم الهاتف مستخدم مسبقاً في بيانات مراجع اخر")
            if will_go:
                self.go_to_patient(patient_data_c2['id'])
            return False
        for check, message in [Validator().validate_name(name),
                               Validator().validate_date(birth_date, "تاريخ الميلاد", past=True),
                               Validator().validate_phone(phone, True),
                               Validator().validate_option(gender, "جنس المراجع مطلوب"),
                               Validator().validate_occupation(occupation),
                               Validator().validate_height(tall),
                               Validator().validate_weight(weight),
                               Validator().validate_doctor_name(doctor),
                               Validator().validate_date(visit_date, "تاريخ الزيارة", future=True)
                               ]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return False
        return True
