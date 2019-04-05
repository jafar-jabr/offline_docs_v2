from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from src.Elements.MyCheckBox import CheckBox
from src.Elements.PathSelector import PathSelector
from src.Elements.RegularButton import RegularButton
from src.models.SharedFunctions import SharedFunctions


class PatientPrintModal(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.show_logo = False
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("prescription_print_modal")
        self.line_width = 480
        self.selected_path = ''
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)

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

        location_label = QLabel("حفظ الى :")
        desktop_path = SharedFunctions.get_desktop_path()
        path_select = PathSelector(300, desktop_path)
        path_line = QHBoxLayout()
        path_line.addWidget(location_label)
        path_line.addWidget(path_select)

        path_q = QWidget()
        path_q.setLayout(path_line)

        exportBtn.clicked.connect(lambda: self.do_export(logo, path_select.value()))
        self.layout.addWidget(path_q)
        self.layout.addWidget(btnLineQ)

        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(500, 100)
        self.setWindowTitle("خيارات الطباعة")

    def do_export(self, logo, select_path):
        self.selected_path = select_path
        if not logo.isChecked():
            self.show_logo = False
        else:
            self.show_logo = True
        self.accept()
