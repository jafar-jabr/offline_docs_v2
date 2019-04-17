from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QGridLayout, QHBoxLayout, QWidget, QCheckBox, QVBoxLayout

from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.ClickableLabel import ClickableLabel, ForgotPasswordLabel
from src.Elements.CustomLabel import RegularLabel, HeadLineLabel
from src.Elements.MyCheckBox import CheckBox
from src.Elements.RegularButton import RegularButton
from src.modals.createAccountModal import CreateAccountModal
from src.models.AppFonts import RegularFont
from src.models.DatabaseModel import Database
from src.models.MyEnc import do_encrypt
from src.models.SessionWrapper import SessionWrapper
from src.Elements.MessageBoxes import MessageBoxes
from src.models.SharedFunctions import SharedFunctions


class Login(QDialog):
    def __init__(self):
        super().__init__()
        window_width = SessionWrapper.get_dimension('login_width')
        window_height = SessionWrapper.get_dimension('login_height')
        app_font = RegularFont()
        self.setFont(app_font)
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("login")
        self.status = "Not Done"
        self.do_order = False
        remember_me_data = Database().get_remember_me()
        user_name_r = remember_me_data['user_name']
        pass_word_r = remember_me_data['pass_word']
        welcomeLabel = HeadLineLabel('                             Welcome !')
        userNameLabel = RegularLabel('Email :')
        # userNameLabel.setFixedWidth(100)
        userNameLabel.setObjectName("user_name_label")
        passWordLabel = RegularLabel('Password :')
        # passWordLabel.setFixedWidth(100)
        passWordLabel.setObjectName("pwd_label")
        userNameEdit = QLineEdit()
        userNameEdit.setObjectName("user_name_input")
        userNameEdit.setFixedWidth(250)
        userNameEdit.setText(user_name_r)
        passWordEdit = QLineEdit()
        passWordEdit.setObjectName("pwd_input")
        passWordEdit.setText(pass_word_r)
        passWordEdit.setFixedWidth(250)
        passWordEdit.setEchoMode(QLineEdit.Password)
        passWordEdit.returnPressed.connect(lambda: self.handleLogin(userNameEdit.text(), passWordEdit.text()))

        self.column = QVBoxLayout()

        self.column.setContentsMargins(220, 10, 0, 0)

        just_widget = QWidget()

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.setColumnStretch(2, 5) #column strech

        # grid.addWidget(welcomeLabel, 1, 0)

        grid.addWidget(userNameLabel, 1, 0) #( row, column)
        grid.addWidget(userNameEdit, 1, 1)

        grid.addWidget(passWordLabel, 2, 0)
        grid.addWidget(passWordEdit, 2, 1)

        btn_line = QHBoxLayout()

        btn_line.setContentsMargins(120, 20, 280, 20)
        btn_line.setSpacing(40)
        self.buttonLogin = ClickableIcon(150, 40, "resources/assets/images/Login/login-button.png")
        self.buttonLogin.clicked.connect(lambda: self.handleLogin(userNameEdit.text(), passWordEdit.text()))

        self.buttonRegister = ClickableIcon(150, 40, "resources/assets/images/Login/register-button.png")
        self.buttonRegister.clicked.connect(lambda: self.handleLogin(userNameEdit.text(), passWordEdit.text()))
        btn_line.addWidget(self.buttonLogin)
        btn_line.addWidget(self.buttonRegister)

        self.remember_me = CheckBox("Remember Me !")
        if len(user_name_r) > 2:
            self.remember_me.setChecked(True)
        sign_up_section = QHBoxLayout()
        sign_up_section.setSpacing(80)
        sign_up_section.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)
        forgot_label = ForgotPasswordLabel('<a href="#" style="color: #000">Forgot Password</a>')
        forgot_label.clicked.connect(self.create_account)
        sign_up_section.addWidget(self.remember_me)
        sign_up_section.addWidget(forgot_label)
        sign_up_Q = QWidget()
        sign_up_Q.setFixedHeight(60)
        sign_up_Q.setLayout(sign_up_section)
        just_widget.setLayout(grid)

        self.column.addWidget(welcomeLabel)
        self.column.addWidget(just_widget)
        self.column.addWidget(sign_up_Q)
        self.column.addLayout(btn_line)
        self.resize(502, 261)
        self.setWindowTitle("Offline Docs / Sign In")
        self.setLayout(self.column)

    def handleLogin(self, email, password):
        enc_pass = do_encrypt(password)
        check = Database().new_check_login(email)
        if check and check["password"] == enc_pass:
            self.status = "Done"
            SessionWrapper.user_password = enc_pass
            SessionWrapper.user_id = check["id"]
            SessionWrapper.user_email = check["email"]
            SessionWrapper.clinic_id = check["clinic_id"]
            SessionWrapper.user_since = check["created_at"]
            SessionWrapper.user_name = check["user_name"]
            SessionWrapper.user_job = SessionWrapper.all_the_jobs[check["job"]]
            SessionWrapper.user_phone = check['phone']
            SessionWrapper.user_role_number = check["role"]
            SessionWrapper.user_role_name = SessionWrapper.all_the_roles[check["role"]]
            self.get_preferences(check["id"])
            if self.remember_me.checkState() == Qt.Checked:
                Database().update_remember_me(email, password)
            else:
                Database().update_remember_me()
            check_point, self.do_order = SharedFunctions.check_point()
            if not check_point:
                self.status = "expired"
            self.accept()
        elif check and not check["password"]:
            SessionWrapper.user_id = check["id"]
            self.status = "New"
            self.accept()
        else:
            MessageBoxes.warning_message("Error", "Invalid Credential")
        return

    def create_account(self):
        CreateAccountModal()

    def get_preferences(self, user_id):
        pref = Database().get_preferences(user_id)
        SessionWrapper.font_color = pref['font_color']
        SessionWrapper.regular_size = pref['regular_size']
        SessionWrapper.big_size = pref['big_size']
        SessionWrapper.app_mode = pref['app_mode']
        SessionWrapper.main_doctor_id = pref['main_doctor_id']
