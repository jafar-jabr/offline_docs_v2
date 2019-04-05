from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.Elements.CustomLabel import HeadLineLabel
from src.dataTables.mainDataTable import MainDataTable
from src.dataTables.mainDataTableMulti import MainDataTableMulti
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.UserBlock import UserBlock


class LandingForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.landing_layout = QVBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 20, 50) #(left, top, right, bottom)
        self.landing_layout.setSpacing(20)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def initUI(self):
        UserBlock(self)
        clinic_id = SessionWrapper.clinic_id
        clinic_info_d = Database().get_clinic_info(clinic_id)
        clinic_name_d = clinic_info_d["clinic_name"]
        clinic_specialization_d = clinic_info_d["specialization"]
        clinic_since_d = clinic_info_d["since"]
        clinic_info = QVBoxLayout()
        clinic_info.setSpacing(15)
        clinic_info_q = QWidget()
        clinic_info.setAlignment(Qt.AlignTop)
        clinic_info.setContentsMargins(0, 30, 40, 0) #(left, top, right, bottom)
        clinicNameLabel = HeadLineLabel('    اسم المؤسسه : '+clinic_name_d)
        clinic_info.addWidget(clinicNameLabel)

        if SessionWrapper.app_mode == 1:
            dd = SharedFunctions.get_main_doctor()
            doctor_name_label = HeadLineLabel('    الدكتور : '+dd)
            clinic_info.addWidget(doctor_name_label)
        specializationLabel = HeadLineLabel('    التخصص : '+clinic_specialization_d)
        clinic_info.addWidget(specializationLabel)
        clinic_info_q.setLayout(clinic_info)
        clinic_info_q.setMaximumHeight(int(self.pc_height * 0.2))
        self.landing_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        self.landing_layout.addWidget(clinic_info_q)
        if SessionWrapper.app_mode == 1:
            the_table = MainDataTable(self.parent)
        else:
            the_table = MainDataTableMulti(self.parent)
        self.landing_layout.addWidget(the_table)
        self.setLayout(self.landing_layout)
        # self.setS
