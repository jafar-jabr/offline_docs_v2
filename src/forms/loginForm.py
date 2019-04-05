from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QGridLayout, QHBoxLayout, QWidget, QCheckBox, QVBoxLayout
from src.Elements.ClickableLabel import ClickableLabel
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
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("login")
        self.status = "Not Done"
        self.do_order = False
        remember_me_data = Database().get_remember_me()
        user_name_r = remember_me_data['user_name']
        pass_word_r = remember_me_data['pass_word']
        welcomeLabel = QLabel('أهلاً بكم')
        userNameLabel = QLabel('Email :')
        # userNameLabel.setFixedWidth(40)
        userNameLabel.setObjectName("user_name_label")
        passWordLabel = QLabel('Password :')
        # passWordLabel.setFixedWidth(40)
        passWordLabel.setObjectName("pwd_label")
        userNameEdit = QLineEdit()
        userNameEdit.setObjectName("user_name_input")
        userNameEdit.setText(user_name_r)
        passWordEdit = QLineEdit()
        passWordEdit.setObjectName("pwd_input")
        passWordEdit.setText(pass_word_r)
        passWordEdit.setEchoMode(QLineEdit.Password)
        passWordEdit.returnPressed.connect(lambda: self.handleLogin(userNameEdit.text(), passWordEdit.text()))
        buttonLogin = RegularButton('Login')
        buttonLogin.clicked.connect(lambda: self.handleLogin(userNameEdit.text(), passWordEdit.text()))

        grid = QGridLayout()
        grid.setSpacing(5)
        grid.setColumnStretch(2, 5) #column strech

        # grid.addWidget(welcomeLabel, 1, 0)

        grid.addWidget(userNameLabel, 1, 0) #( row, column)
        grid.addWidget(userNameEdit, 1, 1)

        grid.addWidget(passWordLabel, 2, 0)
        grid.addWidget(passWordEdit, 2, 1)

        grid.addWidget(buttonLogin, 4, 1)
        self.remember_me = CheckBox("Remember Me !")
        if len(user_name_r) > 2:
            self.remember_me.setChecked(True)
        sign_up_section = QVBoxLayout()
        sign_up_section.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)
        create_acc_label = ClickableLabel('<a href="#" style="color: #ffffff">Create Account</a>')
        create_acc_label.setFixedWidth(160)
        create_acc_label.clicked.connect(self.create_account)
        sign_up_section.addWidget(create_acc_label)
        sign_up_section.addWidget(self.remember_me)
        sign_up_Q = QWidget()
        sign_up_Q.setFixedHeight(60)
        sign_up_Q.setLayout(sign_up_section)
        grid.addWidget(sign_up_Q, 5, 1)

        self.resize(window_width, window_height)
        self.setWindowTitle("Offline Docs / Sign In")
        self.setLayout(grid)

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
