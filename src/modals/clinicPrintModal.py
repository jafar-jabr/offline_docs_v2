from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from src.Elements.CustomLabel import RegularLabel
from src.Elements.DateWidget import DateWidget
from src.Elements.ImageSelector import ImageSelector
from src.Elements.MessageBoxes import MessageBoxes
from datetime import datetime, timedelta

from src.Elements.MyCheckBox import CheckBox
from src.Elements.PathSelector import PathSelector
from src.Elements.RegularButton import RegularButton
from src.Elements.VisitDateWidget import VisitDateWidget
from src.models.SharedFunctions import SharedFunctions
from src.models.Validator import Validator


class ClinicPrintModal(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.the_from = ''
        self.selected_path = ''
        self.the_to = ''
        self.show_logo = False
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("prescription_print_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)

        from_label = RegularLabel('من :')
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        self.from_date = DateWidget(-5, 10, value=yesterday)
        to_label = RegularLabel('الى :')
        self.to_date = VisitDateWidget(-5, 10)

        btnLine = QHBoxLayout()
        # btnLine.setSpacing(40)
        btnLine.setContentsMargins(10, 20, 0, 0)  # (left, top, right, bottom)
        exportBtn = RegularButton('تصدير الى Microsoft Word')
        exportBtn.setMaximumWidth(200)
        logo = CheckBox("تضمين صورة الشعار")
        # logo.setChecked(True)

        btnLine.addWidget(logo)
        btnLine.addWidget(exportBtn)

        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)

        self.layout.addWidget(from_label)
        self.layout.addWidget(self.from_date)

        # self.layout.addWidget(space_label)
        self.layout.addWidget(to_label)
        self.layout.addWidget(self.to_date)

        location_label = QLabel("حفظ الى :")
        desktop_path = SharedFunctions.get_desktop_path()
        path_select = PathSelector(300, desktop_path)
        path_line = QHBoxLayout()
        path_line.addWidget(location_label)
        path_line.addWidget(path_select)

        path_q = QWidget()
        path_q.setLayout(path_line)

        self.layout.addWidget(path_q)

        self.layout.addWidget(btnLineQ)

        exportBtn.clicked.connect(lambda: self.do_export(self.from_date.value(), self.to_date.value(), logo, path_select.value()))

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(500, 350)
        self.setWindowTitle("خيارات الطباعة")

    def do_export(self, from_date, to_date, logo, selected_path):
        self.the_from = from_date
        self.the_to = to_date
        self.selected_path = selected_path
        check, message = Validator.validate_from_to_date(from_date, to_date)
        if not check:
            MessageBoxes.warning_message("خطأ", message)
            return
        if not logo.isChecked():
            self.show_logo = False
        else:
            self.show_logo = True
        self.accept()
