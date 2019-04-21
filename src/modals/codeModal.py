from datetime import datetime, timedelta

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextBox import RegularTextBoxAR
from src.models.DatabaseModel import Database
from src.models.MyEnc import do_decrypt, do_encrypt
from src.models.SharedFunctions import SharedFunctions


class CodeModal(QDialog):
    def __init__(self, title):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("code_modal")
        self.line_width = 480
        self.is_done = False
        self.days_number = 365
        body = QVBoxLayout()

        code_label = RegularLabel('ادخل كود التفعيل')

        code_input = RegularTextBoxAR(300)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(40, 0, 40, 0)  # (left, top, right, bottom)
        saveBtn = RegularButton('تفعيل')
        saveBtn.setMaximumWidth(150)
        saveBtn.clicked.connect(lambda: self.do_activation(code_input.text()))

        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        body.addWidget(code_label)

        body.addWidget(code_input)

        body.addWidget(btnLineQ)

        self.resize(400, 170)
        self.setWindowTitle(title)
        self.setLayout(body)

    def do_activation(self, activation_code):
        app_settings = Database().read_app_settings()
        is_trial = app_settings['field1']
        trial_start_time = app_settings['field2']
        paid_start_time = app_settings['field3']
        rows_limit = app_settings['field4']
        pc_id = app_settings['field5']
        default_lng = app_settings['field6']
        code_origin = do_decrypt(app_settings['field7'])
        waiting_for_code = int(app_settings['field9'])
        if activation_code == code_origin:
            if waiting_for_code == 1:
                subscription_date_string = SharedFunctions.get_date_from_code(activation_code)
                subscription_date_object = datetime.strptime(subscription_date_string, "%d-%m-%Y")
                paid_due = subscription_date_object + timedelta(366)
                the_now = datetime.now()
                self.days_number = SharedFunctions.days_between(the_now, paid_due)
                enc_date = do_encrypt(subscription_date_string)
                Database().make_subscription(activation_code, enc_date)
                self.is_done = True
                self.accept()
            else:
                MessageBoxes.warning_message('خطأ', 'كود التفعيل مستخدم')
        else:
            plain_pc_id = do_decrypt(pc_id)
            check1 = plain_pc_id[3] == activation_code[3]
            check2 = plain_pc_id[7] == activation_code[7]
            check3 = plain_pc_id[4] == activation_code[11]
            check4 = plain_pc_id[8] == activation_code[15]
            if check1 and check2 and check3 and check4:
                subscription_date_string = SharedFunctions.get_date_from_code(activation_code)
                subscription_date_object = datetime.strptime(subscription_date_string, "%d-%m-%Y")
                paid_due = subscription_date_object + timedelta(366)
                the_now = datetime.now()
                self.days_number = SharedFunctions.days_between(the_now, paid_due)
                enc_date = do_encrypt(subscription_date_string)
                Database().make_subscription(activation_code, enc_date)
                self.is_done = True
                self.accept()
            else:
                MessageBoxes.warning_message('خطأ', 'كود التفعيل غير صالح')
