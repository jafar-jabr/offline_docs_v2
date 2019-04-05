from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.PwdTextBoxAR import PwdTextBoxAR
from src.Elements.RegularButton import RegularButton
from src.models.DatabaseModel import Database
from src.models.MyEnc import do_encrypt
from src.models.SessionWrapper import SessionWrapper


class ChangePasswordModal(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("change_password")
        self.line_width = 480
        body = QVBoxLayout()

        pwdH = QHBoxLayout()
        pwdLabel = RegularLabel('كلمة المرور الحالية :')
        pwdEdit = PwdTextBoxAR()
        pwdH.addWidget(pwdLabel)
        pwdH.addWidget(pwdEdit)
        pwdH.setSpacing(10)
        pwdQ = QWidget()
        pwdQ.setLayout(pwdH)
        pwdQ.setFixedWidth(self.line_width)

        pwd_n_1_H = QHBoxLayout()
        pwd_n_1_Label = RegularLabel('كلمة المرور الجديدة :')
        pwd_n_1_Edit = PwdTextBoxAR()
        pwd_n_1_H.addWidget(pwd_n_1_Label)
        pwd_n_1_H.addWidget(pwd_n_1_Edit)
        pwd_n_1_H.setSpacing(10)
        pwd_n_1_Q = QWidget()
        pwd_n_1_Q.setLayout(pwd_n_1_H)
        pwd_n_1_Q.setFixedWidth(self.line_width)

        pwd_n_2_H = QHBoxLayout()
        pwd_n_2_Label = RegularLabel('تأكيد كلمة المرور :')
        pwd_n_2_Edit = PwdTextBoxAR()
        pwd_n_2_H.addWidget(pwd_n_2_Label)
        pwd_n_2_H.addWidget(pwd_n_2_Edit)
        pwd_n_2_H.setSpacing(10)
        pwd_n_2_Q = QWidget()
        pwd_n_2_Q.setLayout(pwd_n_2_H)
        pwd_n_2_Q.setFixedWidth(self.line_width)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(40, 0, 350, 0)  # (left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.setMaximumWidth(100)
        saveBtn.clicked.connect(lambda: self.do_update_password(pwdEdit.text(), pwd_n_1_Edit.text(), pwd_n_2_Edit.text()))

        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        body.addWidget(pwdQ)
        body.addWidget(pwd_n_1_Q)
        body.addWidget(pwd_n_2_Q)
        body.addWidget(btnLineQ)

        self.resize(400, 370)
        self.setWindowTitle("تغيير كلمة المرور")
        self.setLayout(body)
        self.exec_()

    def do_update_password(self, current_pwd, new_pwd_1, new_pwd_2):
        user_id = SessionWrapper.user_id
        enc_pass = do_encrypt(current_pwd)
        if enc_pass == SessionWrapper.user_password:
            if len(new_pwd_1) < 6:
                MessageBoxes.warning_message("خطأ", "كلمة المرور قصيرة جداً")
            elif new_pwd_1 == new_pwd_2:
                the_new_pwd = do_encrypt(new_pwd_1)
                Database().update_my_pwd(user_id, the_new_pwd)
                MessageBoxes.success_message("تحديث", "تم تحديث كلمة المرور")
                self.accept()
            else:
                MessageBoxes.warning_message("خطأ", "كلمة المرور الجديدة وتأكيدها غير متطابقين")
        else:
            MessageBoxes.warning_message("خطأ", "كلمة المرور الحالية غير صحيحة")
