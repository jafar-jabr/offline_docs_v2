from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.Elements.RegularTextBox import RegularTextBoxAR
from src.Elements.filteredCompoBox import FilteredCombo
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.Validator import Validator


class EditStaffModal(QDialog):
    def __init__(self, staff_id):
        super().__init__()
        self.status = "Not Done"
        self.staff_id = staff_id
        staff_data = Database().select_staff_by_id(staff_id)
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("edit_staff_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        nameH = QHBoxLayout()
        nameLabel = RegularLabel('الاسم :')
        nameEdit = RegularTextBoxAR(text=staff_data["the_name"])
        nameEdit.setMaximumWidth(260)
        nameH.addWidget(nameLabel)
        nameH.addWidget(nameEdit)
        nameH.setSpacing(20)
        nameQ = QWidget()
        nameQ.setLayout(nameH)
        nameQ.setFixedWidth(self.line_width - 10)

        phoneH = QHBoxLayout()
        phoneLabel = RegularLabel('رقم الهاتف :')
        phoneEdit = RegularTextBoxAR(text=staff_data["phone"])
        phoneEdit.setMaximumWidth(260)
        phoneH.addWidget(phoneLabel)
        phoneH.addWidget(phoneEdit)
        phoneH.setSpacing(20)
        phoneQ = QWidget()
        phoneQ.setLayout(phoneH)
        phoneQ.setFixedWidth(self.line_width - 10)

        job_title_H = QHBoxLayout()

        job_id = int(staff_data["job"])
        job = SessionWrapper.all_the_jobs[job_id]
        job_title_Label = RegularLabel('العنوان الوظيفي : ' + job)

        job_title_H.addWidget(job_title_Label)
        job_title_H.setSpacing(15)
        job_title_Q = QWidget()
        job_title_Q.setLayout(job_title_H)
        job_title_Q.setFixedWidth(self.line_width - 10)

        self.specializationQ = QWidget()
        specializationV = QVBoxLayout()

        if staff_data["job"] == 1:
            specializationEdit = RegularLabel('الاختصاص : ' + staff_data["specialization"])
            specializationEdit.setWordWrap(True)
        else:
            specializationEdit = RegularLabel()
        specializationV.addWidget(specializationEdit)
        self.specializationQ.setLayout(specializationV)
        self.specializationQ.setFixedWidth(400)

        role_H = QHBoxLayout()
        role_Label = RegularLabel('الصلاحيات :')
        role_options = ["اختر", "مدير", "مستخدم"]
        role_select = FilteredCombo(role_options)
        role_id = int(staff_data["role"])
        role = SessionWrapper.all_the_roles[role_id]
        role_select.setCurrentText(role)
        role_select.setFixedWidth(260)
        role_H.addWidget(role_Label)
        role_H.addWidget(role_select)
        role_H.setSpacing(15)
        role_Q = QWidget()
        role_Q.setLayout(role_H)
        role_Q.setFixedWidth(self.line_width - 10)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(0, 0, 350, 0)  # (left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.clicked.connect(lambda: self.do_add_staff(nameEdit.text(), phoneEdit.text(),
                                                          role_select.currentText()))
        saveBtn.setMaximumWidth(100)

        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        self.layout.addWidget(nameQ)
        self.layout.addWidget(phoneQ)
        self.layout.addWidget(role_Q)
        self.layout.addWidget(job_title_Q)
        self.layout.addWidget(self.specializationQ)
        self.layout.addWidget(btnLineQ)
        if staff_data["job"] != 1:
            self.specializationQ.hide()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(600, 400)
        self.setWindowTitle("تحديث البيانات")
        self.exec_()

    def job_title_changed(self):
        selection = self.sender().currentText()
        if selection == "طبيب":
            self.specializationQ.show()
        else:
            self.specializationQ.hide()

    def do_add_staff(self, name, phone, role):
        for check, message in [Validator().validate_name(name),
                               Validator().validate_phone(phone),
                               Validator().validate_option(role, "الصلاحيات مطلوبة !")
                               ]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        staff_id = self.staff_id
        name_exist = Database().check_if_other_staff_name_exist(name, staff_id)
        phone_exist = Database().check_if_other_staff_phone_exist(phone, staff_id)
        if name_exist:
            MessageBoxes.warning_message("خطأ", "الاسم موجود مسبقاً في جدول المنتسبين")
            return
        if phone_exist and len(phone) > 0:
            MessageBoxes.warning_message("خطأ", "رقم الهاتف مستخدم مسبقاً في بيانات منتسب اخر")
            return

        role_id = SessionWrapper.all_the_roles_ids[role]

        Database().update_staff(staff_id, name, phone, role_id)
        MessageBoxes.success_message("تأكيد!", "تم تحديث بيانات المنتسب")
        self.status = "Done"
        self.accept()
