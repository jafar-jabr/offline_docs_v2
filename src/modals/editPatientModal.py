from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QGridLayout

from src.Elements.CustomLabel import RegularLabel
from src.Elements.DateWidget import DateWidget
from src.Elements.IconTextBoxAR import IconTextBoxAR
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.Elements.RegularTextBoxAR import RegularTextBoxAR
from src.Elements.filteredCompoBox import FilteredCombo
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.Validator import Validator


class EditPatientModal(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.status = ''
        self.other_patient_id = 0
        self.patient_id = parent.patient_id
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.parent = parent
        data = Database().get_patient_by_id(self.parent.patient_id)
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("edit_patient_modal")
        self.line_width = int(self.pc_width * 0.3)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 20)  # (left, top, right, bottom)

        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(3, 2)  # column, strech
        #
        nameLabel = RegularLabel('اسم المراجع :')
        self.nameEdit = IconTextBoxAR()
        self.nameEdit.setText(data['patient_name'])
        self.nameEdit.setFixedWidth(242)
        self.nameEdit.iconClicked.connect(lambda: self.check_user(self.nameEdit.text()))
        first_grid.addWidget(nameLabel, 1, 0)  # ( row, column)
        first_grid.addWidget(self.nameEdit, 1, 1)
        #
        birthDateLabel = RegularLabel('تاريخ الميلاد :')
        self.birthdateEdit = DateWidget(0, 100, value=data["birth_date"])

        first_grid.addWidget(birthDateLabel, 2, 0)  # ( row, column)
        first_grid.addWidget(self.birthdateEdit, 2, 1)

        phoneLabel = RegularLabel('رقم الهاتف ( اختياري ) :')
        self.phoneEdit = RegularTextBoxAR(text=data["phone"])
        self.phoneEdit.setFixedWidth(235)

        first_grid.addWidget(phoneLabel, 3, 0)  # ( row, column)
        first_grid.addWidget(self.phoneEdit, 3, 1)

        genderLabel = RegularLabel('الجنس :')
        genderLabel.setWidth(200)
        gender_options = ["اختر", "انثى", "ذكر"]
        self.gender_select = FilteredCombo(gender_options)
        self.gender_select.setCurrentText(data["gender"])

        first_grid.addWidget(genderLabel, 4, 0)  # ( row, column)
        first_grid.addWidget(self.gender_select, 4, 1)

        occupationLabel = RegularLabel('العمل ( اختياري ) :')
        occupationLabel.setWidth(200)

        self.occupation_input = RegularTextBoxAR(240, text=data['occupation'])

        first_grid.addWidget(occupationLabel, 5, 0)  # ( row, column)
        first_grid.addWidget(self.occupation_input, 5, 1)

        tall_label = RegularLabel('الطول (اختياري) :')
        tall_label.setWidth(100)
        tall_edit_h = QHBoxLayout()
        tall_edit_h.setContentsMargins(0, 0, 0, 0)
        self.tall_edit = RegularTextBoxAR(text=data['tall'])
        self.tall_edit.setValidator(QIntValidator())
        self.tall_edit.setFixedWidth(235)
        tall_unit = RegularLabel('<i style="font-size: 14px">سم</i>')
        tall_edit_h.addWidget(self.tall_edit)
        tall_edit_h.addWidget(tall_unit)
        tall_q = QWidget()
        tall_q.setLayout(tall_edit_h)
        first_grid.addWidget(tall_label, 6, 0)  # ( row, column)
        first_grid.addWidget(tall_q, 6, 1)
        # first_grid.addWidget(tall_unit, 4, 2)

        weight_label = RegularLabel('الوزن ( اختياري ) :')
        weight_label.setWidth(100)
        weight_edit_h = QHBoxLayout()
        weight_edit_h.setContentsMargins(0, 0, 0, 0)
        weight_edit_q = QWidget()
        self.weight_edit = RegularTextBoxAR(text=data['weight'])
        self.weight_edit.setValidator(QIntValidator())
        self.weight_edit.setFixedWidth(235)
        weight_unit = RegularLabel('<i style="font-size: 14px">كغم</i>')
        weight_edit_h.addWidget(self.weight_edit)
        weight_edit_h.addWidget(weight_unit)
        weight_edit_q.setLayout(weight_edit_h)

        first_grid.addWidget(weight_label, 7, 0)  # ( row, column)
        first_grid.addWidget(weight_edit_q, 7, 1)
        about_l = RegularLabel('حول ( اختياري ) :')
        about_l.setWidth(100)
        self.about_f = RegularTextArea(90, int(self.pc_width * 0.4), text=data["about"],
                                       placeHolder="معلومات تخص التاريخ المرضي للمراجع (ان وجدت)")
        first_grid.addWidget(about_l, 8, 0)  # ( row, column)
        first_grid.addWidget(self.about_f, 8, 1)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(40, 0, int(self.pc_width * 0.18), 20)  # (left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.setMaximumWidth(100)
        saveBtn.clicked.connect(lambda: self.do_update_patient(self.nameEdit.text(), self.birthdateEdit.value(),
                                                               self.gender_select.currentText(),
                                                               self.occupation_input.text(),
                                                               self.weight_edit.text(),
                                                               self.tall_edit.text(),
                                                               self.phoneEdit.text(), self.about_f.toPlainText()))
        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)
        btnLineQ.setFixedWidth(int(self.pc_width * 0.45))
        self.layout.addLayout(first_grid)
        self.layout.addWidget(self.about_f)
        self.layout.addWidget(btnLineQ)
        self.setLayout(self.layout)
        self.resize(int(self.pc_width * 0.6), int(self.pc_height * 0.5))
        self.setWindowTitle("تعديل بيانات المراجع")

    def check_user(self, the_name):
        check, message = Validator().validate_name(the_name)
        if not check:
            MessageBoxes.warning_message("خطأ", message)
        else:
            name_exist, patient_data_c = Database().check_if_other_patient_name_exist(the_name, self.patient_id)
            if name_exist:
                will_go = MessageBoxes.patient_exist("خطأ", "الاسم موجود مسبقاً في جدول المراجعين")
                if will_go:
                    self.go_to_patient(patient_data_c['id'])
                return
            else:
                MessageBoxes.success_message("جديد", "الاسم غير مستعمل مسبقاً")

    def go_to_patient(self, patient_id):
        self.status = 'Redirect'
        self.other_patient_id = patient_id
        self.accept()

    def reset_form(self):
        self.nameEdit.setText("")
        self.phoneEdit.setText("")
        self.aboutBody.setPlainText("")
        # self.doctor_select.setCurrentText("اختر")

    def do_update_patient(self, name, birth_date, gender, occupation, weight, height, phone, about):
        for check, message in [Validator().validate_name(name),
                               Validator().validate_option(gender, "جنس المراجع مطلوب"),
                               Validator().validate_occupation(occupation),
                               Validator().validate_height(height),
                               Validator().validate_weight(weight),
                               Validator().validate_phone(phone, True),
                               Validator().validate_date(birth_date, "تاريخ الميلاد", past=True),
                               ]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return

        name_exist, patient_data_c = Database().check_if_other_patient_name_exist(name, self.patient_id)
        phone_exist, patient_data_c2 = Database().check_if_other_patient_phone_exist(phone, self.patient_id)
        if name_exist:
            will_go = MessageBoxes.patient_exist("خطأ", "الاسم موجود مسبقاً في جدول المراجعين")
            if will_go:
                self.go_to_patient(patient_data_c['id'])
            return
        if phone_exist and len(phone) > 0:
            will_go = MessageBoxes.patient_exist("خطأ", "رقم الهاتف مستخدم مسبقاً في بيانات مراجع اخر")
            if will_go:
                self.go_to_patient(patient_data_c2['id'])
            return
        Database().update_only_patient(self.patient_id, name, birth_date, gender, occupation, weight, height, phone, about)
        MessageBoxes.success_message("تأكيد!", "تم تحديث البيانات")
        self.status = 'Done'
        self.accept()
