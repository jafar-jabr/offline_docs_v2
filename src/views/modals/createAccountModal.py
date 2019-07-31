from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QLineEdit
from src.views.widgets.CustomLabel import RegularLabel
from src.views.widgets.MessageBoxes import MessageBoxes
from src.views.widgets.RegularButton import RegularButton
from src.views.widgets.RegularTextBox import RegularTextBox
from src.models.DatabaseModel import Database
from src.models.MyEnc import do_encrypt
from src.models.GenericFunctions import SharedFunctions
from src.models.Validator import Validator


class CreateAccountModal(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("create_account_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.result = "try"
        self.registered_email = ""
        self.registered_password = ""
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        noteLabel = RegularLabel('Create New Account')
        nameH = QHBoxLayout()
        nameLabel = RegularLabel('Name :')
        nameEdit = RegularTextBox()
        nameEdit.setMaximumWidth(273)
        nameH.addWidget(nameLabel)
        nameH.addWidget(nameEdit)
        nameH.setSpacing(20)
        nameQ = QWidget()
        nameQ.setLayout(nameH)
        nameQ.setFixedWidth(self.line_width)
        
        emailH = QHBoxLayout()
        emailLabel = RegularLabel('Email :')
        emailEdit = RegularTextBox()
        emailEdit.setMaximumWidth(260)
        emailH.addWidget(emailLabel)
        emailH.addWidget(emailEdit)
        emailH.setSpacing(20)
        emailQ = QWidget()
        emailQ.setLayout(emailH)
        emailQ.setFixedWidth(self.line_width - 10)

        password_first_q = QWidget()
        password_first_H = QHBoxLayout()
        password_first_Label = RegularLabel('Password:')
        passWordEdit = QLineEdit()
        passWordEdit.setObjectName("pwd_input")
        passWordEdit.setFixedWidth(250)
        passWordEdit.setEchoMode(QLineEdit.Password)
        password_first_H.addWidget(password_first_Label)
        password_first_H.addWidget(passWordEdit)
        password_first_q.setLayout(password_first_H)

        password_confirm_q = QWidget()
        password_c_h = QHBoxLayout()
        specializationLabel = RegularLabel('confirm Password:')
        passWordEdit_2 = QLineEdit()
        passWordEdit_2.setObjectName("pwd_input_2")
        passWordEdit_2.setFixedWidth(250)
        passWordEdit_2.setEchoMode(QLineEdit.Password)
        password_c_h.addWidget(specializationLabel)
        password_c_h.addWidget(passWordEdit_2)
        password_confirm_q.setLayout(password_c_h)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(0, 0, 350, 0)  # (left, top, right, bottom)
        saveBtn = RegularButton('Save')
        saveBtn.clicked.connect(lambda: self.do_registration(nameEdit.text(), emailEdit.text(),
                                                          passWordEdit.text(),
                                                          passWordEdit_2.text()))
        saveBtn.setMaximumWidth(100)

        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        self.layout.addWidget(noteLabel)
        self.layout.addWidget(nameQ)
        self.layout.addWidget(emailQ)
        self.layout.addWidget(password_first_q)
        self.layout.addWidget(password_confirm_q)
        self.layout.addWidget(btnLineQ)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(600, 400)
        self.setWindowTitle("Create New Account")

    def do_registration(self, name, email, password, password_2):
        for check, message in [Validator.validate_name(name),
                               Validator.validate_email(email),
                               Validator.validate_passwords(password, password_2)
                               ]:
            if not check:
                MessageBoxes.warning_message("Error", message)
                return
        created_at = SharedFunctions.get_current_date_str()
        first_name, last_name = SharedFunctions.split_the_name(name)
        enc_pass = do_encrypt(password)
        Database().register_user(first_name, last_name, email, enc_pass, created_at)
        MessageBoxes.success_message("Done!", "You singed up successfully now you can sign in")
        self.result = "Done"
        self.registered_email = email
        self.registered_password = password
        self.accept()
