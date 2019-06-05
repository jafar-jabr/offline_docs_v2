from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout

from src.Elements.CustomLabel import RegularLabel
from src.Elements.IconTextBoxAR import IconTextBoxAR
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.Elements.RegularTextBox import RegularTextBoxAR
from src.Elements.filteredCompoBox import FilteredComboBox
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.Validator import Validator


class CreateAccountModal(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("create_account_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        noteLabel = RegularLabel('انشاء نسخة جديدة كلياً من البرنامج, اذا كنت ضمن مؤسسة موجودة مسبقاً اطلب من احد زملائك ان يضيفك')
        nameH = QHBoxLayout()
        nameLabel = RegularLabel('الاسم :')
        nameEdit = IconTextBoxAR()
        nameEdit.iconClicked.connect(self.check_user)
        nameEdit.setMaximumWidth(273)
        nameH.addWidget(nameLabel)
        nameH.addWidget(nameEdit)
        nameH.setSpacing(20)
        nameQ = QWidget()
        nameQ.setLayout(nameH)
        nameQ.setFixedWidth(self.line_width)
        phoneH = QHBoxLayout()
        phoneLabel = RegularLabel('رقم الهاتف :')
        phoneEdit = RegularTextBoxAR()
        phoneEdit.setMaximumWidth(260)
        phoneH.addWidget(phoneLabel)
        phoneH.addWidget(phoneEdit)
        phoneH.setSpacing(20)
        phoneQ = QWidget()
        phoneQ.setLayout(phoneH)
        phoneQ.setFixedWidth(self.line_width - 10)

        job_title_H = QHBoxLayout()
        job_title_Label = RegularLabel('العنوان الوظيفي :')
        job_title_options = ["اختر", "طبيب", "صيدلاني", "ممرض", "اداري", "مساعد"]
        job_title_select = FilteredComboBox(job_title_options)
        job_title_select.activated[str].connect(self.job_title_changed)
        job_title_select.setFixedWidth(260)
        job_title_H.addWidget(job_title_Label)
        job_title_H.addWidget(job_title_select)
        job_title_H.setSpacing(15)
        job_title_Q = QWidget()
        job_title_Q.setLayout(job_title_H)
        job_title_Q.setFixedWidth(self.line_width - 10)

        self.specializationQ = QWidget()
        specializationV = QVBoxLayout()
        specializationLabel = RegularLabel('الاختصاص :')
        specializationV.addWidget(specializationLabel)
        specializationH = QHBoxLayout()
        specializationH.setContentsMargins(0, 0, 50, 0)  # (left, top, right, bottom)
        specializationEdit = RegularTextArea()
        specializationH.addWidget(specializationEdit)
        specializationV.addLayout(specializationH)
        self.specializationQ.setLayout(specializationV)
        self.specializationQ.setFixedWidth(1040)

        role_H = QHBoxLayout()
        role_Label = RegularLabel('الصلاحيات :')
        role_options = ["اختر", "مدير", "مستخدم"]
        role_select = FilteredComboBox(role_options)
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
                                                          job_title_select.currentText(),
                                                          role_select.currentText(),
                                                          specializationEdit.toPlainText()))
        saveBtn.setMaximumWidth(100)

        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        self.layout.addWidget(noteLabel)
        self.layout.addWidget(nameQ)
        self.layout.addWidget(phoneQ)
        self.layout.addWidget(job_title_Q)
        self.layout.addWidget(self.specializationQ)
        self.layout.addWidget(role_Q)
        self.layout.addWidget(btnLineQ)
        self.specializationQ.hide()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(600, 400)
        self.setWindowTitle("انشاء حساب جديد")
        self.exec_()

    def check_user(self):
        pass

    def job_title_changed(self):
        selection = self.sender().currentText()
        if selection == "طبيب":
            self.specializationQ.show()
        else:
            self.specializationQ.hide()

    def do_add_staff(self, name, phone, job, role, specialization=None):
        specialization = (str(specialization)).strip()
        for check, message in [Validator().validate_name(name),
                               Validator().validate_phone(phone),
                               Validator().validate_option(job, "العنوان الوظيفي مطلوب !"),
                               Validator().validate_option(role, "الصلاحيات مطلوبة !"),
                               Validator().validate_specialization(specialization, job)
                               ]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        clinic_id = SessionWrapper.clinic_id
        job_id = SessionWrapper.all_the_jobs_ids[job]
        role_id = SessionWrapper.all_the_roles_ids[role]
        Database().insert_staff(clinic_id, name, phone, job_id, role_id, specialization)
        MessageBoxes.success_message("تأكيد!", "تم اضافة المنتسب, يستطيع الان تسجيل الدخول")
        self.accept()
