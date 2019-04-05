from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.MyCheckBox import CheckBox
from src.Elements.PathSelector import PathSelector
from src.Elements.RegularButton import RegularButton
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class PrescriptionPrintModal(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.selected = []
        self.show_logo = False
        self.selected_path = ''
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("prescription_print_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)

        symptoms = CheckBox("الاعراض")

        diagnosis = CheckBox("التشخيص")

        prescription = CheckBox("الوصفة")
        prescription.setChecked(True)

        recommendations = CheckBox("التوصيات")

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

        self.layout.addWidget(symptoms)
        self.layout.addWidget(diagnosis)
        self.layout.addWidget(prescription)
        self.layout.addWidget(recommendations)

        location_label = QLabel("حفظ الى :")
        desktop_path = SharedFunctions.get_desktop_path()
        path_select = PathSelector(300, desktop_path)
        path_line = QHBoxLayout()
        path_line.addWidget(location_label)
        path_line.addWidget(path_select)

        path_q = QWidget()
        path_q.setLayout(path_line)

        exportBtn.clicked.connect(lambda: self.do_export(symptoms, diagnosis, prescription, recommendations, logo, path_select.value()))
        self.layout.addWidget(path_q)
        self.layout.addWidget(btnLineQ)
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(500, 300)
        self.setWindowTitle("خيارات الطباعة")

    def do_export(self, symptoms, diagnosis, prescription, recommendation, logo, selected_path):
        self.selected_path = selected_path
        if symptoms.isChecked():
            self.selected.append('symptoms')
        if diagnosis.isChecked():
            self.selected.append('diagnosis')
        if prescription.isChecked():
            self.selected.append('prescription')
        if recommendation.isChecked():
            self.selected.append('recommendations')
        if not logo.isChecked():
            self.show_logo = False
        else:
            self.show_logo = True
            clinic_id = SessionWrapper.clinic_id
            logo = SharedFunctions.get_logo_img(clinic_id)
            if not logo:
                MessageBoxes.warning_message("خطأ", "اذا اخترت تضمين صورة الشعار يجب اولاً اضافة الشعار من صفحة الاعدادات")
        if len(self.selected):
            self.accept()
        else:
            MessageBoxes.warning_message("خطأ", "يجب اختيار واحد على الاقل من خيارات الطباعة")
