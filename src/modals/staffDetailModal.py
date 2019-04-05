from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QVBoxLayout

from src.Elements.CustomLabel import RegularLabel
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper


class StaffDetailModal(QDialog):
    def __init__(self, staff_id):
        super().__init__()
        self.staff_id = staff_id
        staff_data = Database().select_staff_by_id(staff_id)
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("staff_details_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        nameH = QHBoxLayout()

        nameLabel = RegularLabel('الاسم : '+staff_data["the_name"])
        nameH.addWidget(nameLabel)
        nameH.setSpacing(20)
        nameQ = QWidget()
        nameQ.setLayout(nameH)
        nameQ.setFixedWidth(self.line_width)
        phoneH = QHBoxLayout()

        phoneLabel = RegularLabel('رقم الهاتف : '+staff_data["phone"])
        phoneH.addWidget(phoneLabel)
        phoneH.setSpacing(20)
        phoneQ = QWidget()
        phoneQ.setLayout(phoneH)
        phoneQ.setFixedWidth(self.line_width - 10)

        job_title_H = QHBoxLayout()

        job_id = int(staff_data["job"])
        job = SessionWrapper.all_the_jobs[job_id]
        job_title_Label = RegularLabel('العنوان الوظيفي : '+job)

        job_title_H.addWidget(job_title_Label)
        job_title_H.setSpacing(15)
        job_title_Q = QWidget()
        job_title_Q.setLayout(job_title_H)
        job_title_Q.setFixedWidth(self.line_width - 10)

        self.specializationQ = QWidget()
        specializationV = QVBoxLayout()

        if staff_data["job"] == 1:
            specializationEdit = RegularLabel('الاختصاص : '+staff_data["specialization"])
            specializationEdit.setWordWrap(True)
        else:
            specializationEdit = RegularLabel()
        specializationV.addWidget(specializationEdit)
        self.specializationQ.setLayout(specializationV)
        self.specializationQ.setFixedWidth(400)

        role_H = QHBoxLayout()
        role_id = int(staff_data["role"])
        role = SessionWrapper.all_the_roles[role_id]
        role_Label = RegularLabel('الصلاحيات : '+role)
        role_H.addWidget(role_Label)

        role_H.setSpacing(15)
        role_Q = QWidget()
        role_Q.setLayout(role_H)
        role_Q.setFixedWidth(self.line_width - 10)

        self.layout.addWidget(nameQ)
        self.layout.addWidget(phoneQ)
        self.layout.addWidget(job_title_Q)
        self.layout.addWidget(self.specializationQ)
        self.layout.addWidget(role_Q)
        if staff_data["job"] != 1:
            self.specializationQ.hide()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)
        self.resize(400, 400)
        self.setWindowTitle("التفاصيل")
        self.exec_()
