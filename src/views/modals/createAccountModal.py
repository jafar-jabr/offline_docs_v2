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
        self.registered_username = ""
        self.registered_password = ""
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        noteLabel = RegularLabel('Create New Account')
        firstNameH = QHBoxLayout()
        lastNameH = QHBoxLayout()
        userNameH = QHBoxLayout()

        userNameLabel = RegularLabel('Username Or Email:')
        userNameEdit = RegularTextBox()
        userNameEdit.setMaximumWidth(273)
        userNameH.addWidget(userNameLabel)
        userNameH.addWidget(userNameEdit)
        userNameH.setSpacing(20)
        userNameQ = QWidget()
        userNameQ.setLayout(userNameH)
        userNameQ.setFixedWidth(self.line_width)

        firstNameLabel = RegularLabel('First Name :')
        firstNameEdit = RegularTextBox()
        firstNameEdit.setMaximumWidth(273)
        firstNameH.addWidget(firstNameLabel)
        firstNameH.addWidget(firstNameEdit)
        firstNameH.setSpacing(20)
        firstNameQ = QWidget()
        firstNameQ.setLayout(firstNameH)
        firstNameQ.setFixedWidth(self.line_width)

        lastNameLabel = RegularLabel('Last Name :')
        lastNameEdit = RegularTextBox()
        lastNameEdit.setMaximumWidth(273)
        lastNameH.addWidget(lastNameLabel)
        lastNameH.addWidget(lastNameEdit)
        lastNameH.setSpacing(20)
        lastNameQ = QWidget()
        lastNameQ.setLayout(lastNameH)
        lastNameQ.setFixedWidth(self.line_width)

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
        saveBtn.clicked.connect(lambda: self.do_registration(firstNameEdit.text(), lastNameEdit.text(), userNameEdit.text(),
                                                          passWordEdit.text(),
                                                          passWordEdit_2.text()))
        saveBtn.setMaximumWidth(100)

        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        self.layout.addWidget(noteLabel)
        self.layout.addWidget(userNameQ)
        self.layout.addWidget(firstNameQ)
        self.layout.addWidget(lastNameQ)
        self.layout.addWidget(password_first_q)
        self.layout.addWidget(password_confirm_q)
        self.layout.addWidget(btnLineQ)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(600, 400)
        self.setWindowTitle("Create New Account")

    def do_registration(self, firstName, lastName, email, password, password_2):
        for check, message in [Validator.validate_name(firstName), Validator.validate_name(lastName),
                               Validator.validate_username(email),
                               Validator.validate_passwords(password, password_2)
                               ]:
            if not check:
                MessageBoxes.warning_message("Error", message)
                return
        created_at = SharedFunctions.get_current_date_str()
        #first_name, last_name = SharedFunctions.split_the_name(name)
        enc_pass = do_encrypt(password)
        Database().register_user(firstName, lastName, email, enc_pass, created_at)
        MessageBoxes.success_message("Done!", "You singed up successfully now you can sign in")
        self.result = "Done"
        self.registered_username = email
        self.registered_password = password
        self.accept()
