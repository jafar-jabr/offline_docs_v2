from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from src.Elements.ClickableLabel import ClickableLabel
from src.Elements.CustomLabel import RegularLabel
from src.Elements.ImageSelector import ImageSelector
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.PwdTextBoxAR import PwdTextBoxAR
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextBox import RegularTextBoxAR
from src.modals.changePasswordModal import ChangePasswordModal
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.UserBlock import UserBlock
from src.models.Validator import Validator


class AccountSettings(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.line_width = int(self.pc_width * 0.3)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 20) #(left, top, right, bottom)
        self.user = UserBlock(self)

        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(3, 2)  # column, strech

        nameLabel = RegularLabel('الاسم :')
        nameEdit = RegularTextBoxAR(text=SessionWrapper.user_name)

        first_grid.addWidget(nameLabel, 1, 0)  # ( row, column)
        first_grid.addWidget(nameEdit, 1, 1)

        emailLabel = RegularLabel('البريد الالكتروني :')
        emailEdit = RegularTextBoxAR(text=SessionWrapper.user_email)

        first_grid.addWidget(emailLabel, 2, 0)  # ( row, column)
        first_grid.addWidget(emailEdit, 2, 1)

        phoneLabel = RegularLabel('رقم الهاتف :')
        phoneEdit = RegularTextBoxAR(text=SessionWrapper.user_phone)

        first_grid.addWidget(phoneLabel, 3, 0)  # ( row, column)
        first_grid.addWidget(phoneEdit, 3, 1)

        pwdLabel = RegularLabel('كلمة المرور :')
        pwdEdit = PwdTextBoxAR(text="any text")
        change_text = '<a href="#" style="color: %s; font-size: 18px;">تغيير</a>' % SessionWrapper.font_color
        pwd_ch_label = ClickableLabel(change_text)
        pwd_ch_label.clicked.connect(self.show_change_password)

        first_grid.addWidget(pwdLabel, 4, 0)  # ( row, column)
        first_grid.addWidget(pwdEdit, 4, 1)
        first_grid.addWidget(pwd_ch_label, 4, 2)

        jobLabel = RegularLabel('العنوان الوظيفي :')
        job_name = RegularTextBoxAR(text=SessionWrapper.user_job)
        job_name.setReadOnly(True)
        read_only_label1 = RegularLabel('<i style="font-size: 14px">للاطلاع فقط</i>')

        first_grid.addWidget(jobLabel, 5, 0)  # ( row, column)
        first_grid.addWidget(job_name, 5, 1)
        first_grid.addWidget(read_only_label1, 5, 2)

        roleLabel = RegularLabel('الصلاحيات :')
        role_name = RegularTextBoxAR(text=SessionWrapper.user_role_name)
        role_name.setReadOnly(True)
        read_only_label2 = RegularLabel('<i style="font-size: 14px">للاطلاع فقط</i>')

        first_grid.addWidget(roleLabel, 6, 0)  # ( row, column)
        first_grid.addWidget(role_name, 6, 1)
        first_grid.addWidget(read_only_label2, 6, 2)

        imageLabel = RegularLabel('الصورة الشخصية :    ')
        image_select = ImageSelector(250)

        first_grid.addWidget(imageLabel, 7, 0)  # ( row, column)
        first_grid.addWidget(image_select, 7, 1)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(self.pc_width * 0.4, 50, 0, 0) #(left, top, right, bottom)

        saveBtn = RegularButton('حفظ')
        saveBtn.setMaximumWidth(100)
        saveBtn.clicked.connect(lambda: self.do_update_info(nameEdit.text(), emailEdit.text(), phoneEdit.text(), image_select.value()))

        btnLine.addWidget(saveBtn)

        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        self.layout.addLayout(first_grid)
        self.layout.addWidget(btnLineQ)

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

    @staticmethod
    def show_change_password():
        ChangePasswordModal()

    def do_update_info(self, name, email, phone, img_path):
        for check, message in [Validator().validate_name(name), Validator().validate_email(email), Validator().validate_phone(phone)]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        if len(img_path) > 3:
            check, message = Validator().validate_image(img_path)
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        user_id = SessionWrapper.user_id
        email_exist = Database().check_if_other_staff_email_exist(email, user_id)
        if email_exist:
            MessageBoxes.warning_message("خطأ", "البريد الإلكتروني مستخدم في بيانات منتسب اخر")
            return
        Database().update_my_info(user_id, name, email, phone)
        SharedFunctions.copy_profile_img(user_id, img_path)
        if len(img_path) > 3:
            self.user.update_image(img_path)
        self.user.update_name(name)
        MessageBoxes.success_message("تأكيد!", "تم تحديث البيانات")
