from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog
from PyQt5.QtCore import Qt

from src.Elements.CustomLabel import RegularLabel
from src.Elements.ImageSelector import ImageSelector
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextBox import RegularTextBoxAR
from src.dataTables.staffDataTable import StaffDataTable
from src.modals.addStaffModal import AddStaffModal
from src.modals.clinicPrintModal import ClinicPrintModal
from src.models.ClinicReport import ClinicReport
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.UserBlock import UserBlock
from src.models.Validator import Validator


class GeneralSettings(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.parent = parent
        self.settings_line_width = int(self.pc_width * 0.3)
        self.layout_general_settings = QVBoxLayout()
        self.layout_general_settings.setAlignment(Qt.AlignTop)
        self.layout_general_settings.setSpacing(15)
        self.layout_general_settings.setContentsMargins(0, 30, 80, 20)  # (left, top, right, bottom)
        self.initUI()

    def initUI(self):
        UserBlock(self)
        clinic_id = SessionWrapper.clinic_id
        clinic_data = Database().get_clinic_info(clinic_id)

        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(2, 2)  # column, strech

        clinic_nameLabel = RegularLabel('اسم المؤسسة :')
        clinic_nameEdit = RegularTextBoxAR(text=clinic_data["clinic_name"])

        first_grid.addWidget(clinic_nameLabel, 1, 0)  # ( row, column)
        first_grid.addWidget(clinic_nameEdit, 1, 1)

        clinic_specialLabel = RegularLabel('الاختصاص :')
        specialEdit = RegularTextBoxAR(text=clinic_data["specialization"])

        first_grid.addWidget(clinic_specialLabel, 2, 0)  # ( row, column)
        first_grid.addWidget(specialEdit, 2, 1)

        clinic_phoneLabel = RegularLabel('رقم الهاتف ( اختياري ) :')
        clinic_phoneEdit = RegularTextBoxAR(text=clinic_data["phone"])

        first_grid.addWidget(clinic_phoneLabel, 3, 0)  # ( row, column)
        first_grid.addWidget(clinic_phoneEdit, 3, 1)

        clinic_logoLabel = RegularLabel('صورة الشعار :')
        logo_line = QHBoxLayout()
        logo_line.setContentsMargins(0, 0, 0, 0)
        logo_line_q = QWidget()
        clinic_logoEdit = ImageSelector(250)
        read_only_label1 = RegularLabel('<i style="font-size: 14px">يستخدم في طباعة التقارير</i>')
        logo_line.addWidget(clinic_logoEdit)
        logo_line.addWidget(read_only_label1)
        logo_line_q.setLayout(logo_line)
        first_grid.addWidget(clinic_logoLabel, 4, 0)  # ( row, column)
        first_grid.addWidget(logo_line_q, 4, 1)

        addressLabel = RegularLabel('العنوان :')
        addressEdit = RegularTextBoxAR(500, text=clinic_data["address"])

        first_grid.addWidget(addressLabel, 5, 0)  # ( row, column)
        first_grid.addWidget(addressEdit, 5, 1)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(0, 0, self.pc_width*0.25, 0) #(left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.clicked.connect(lambda: self.do_update_info(clinic_nameEdit.text(), specialEdit.text(), addressEdit.text(), clinic_phoneEdit.text(), clinic_logoEdit.value()))
        saveBtn.setMaximumWidth(100)

        addBtn = RegularButton('اضافة منتسب')
        addBtn.setMaximumWidth(120)
        addBtn.clicked.connect(self.do_add_staff)

        reportBtn = RegularButton('تقرير')
        reportBtn.setMaximumWidth(100)
        reportBtn.clicked.connect(self.clinic_report)

        btnLine.addWidget(saveBtn)
        btnLine.addWidget(addBtn)
        btnLine.addWidget(reportBtn)

        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)
        btnLineQ.setFixedWidth(self.pc_width-200)

        self.layout_general_settings.addLayout(first_grid)
        self.layout_general_settings.addWidget(btnLineQ)
        self.data_table = StaffDataTable(self.parent)
        self.layout_general_settings.addWidget(self.data_table)

        self.layout_general_settings.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout_general_settings)

    def do_add_staff(self):
        if not SharedFunctions.is_manager():
            MessageBoxes.warning_message("خطأ", "ليس لديك الصلاحية للقيام بذلك")
            return
        try_to_add = AddStaffModal(self).exec_()
        if try_to_add == QDialog.Accepted:
            self.data_table.refresh_data()

    def do_update_info(self, name, specialization, address, phone, img_path=""):
        if not SharedFunctions.is_manager():
            MessageBoxes.warning_message("خطأ", "ليس لديك الصلاحية للقيام بذلك")
            return
        for check, message in [Validator().validate_name(name), Validator().validate_clinic_specialization(specialization), Validator().validate_address(address), Validator().validate_phone(phone)]:
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        if len(img_path) > 3:
            check, message = Validator().validate_image(img_path)
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
        clinic_id = SessionWrapper.clinic_id
        Database().update_clinic_info(clinic_id, name, specialization, address, phone)
        SharedFunctions.copy_logo_img(clinic_id, img_path)
        MessageBoxes.success_message("تأكيد!", "تم تحديث البيانات. ")

    def clinic_report(self):
        modal = ClinicPrintModal(self)
        exe = modal.exec_()
        if exe == QDialog.Accepted:
            first_date = modal.the_from
            last_date = modal.the_to
            show_logo = modal.show_logo
            path_to_save = modal.selected_path
            print(path_to_save)
            ClinicReport(first_date, last_date, show_logo, path_to_save)
