from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from src.Elements.CustomLabel import RegularLabel
from datetime import datetime, timedelta

from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.dateTimeWidget import DateTimeWidget
from src.Elements.secondDateTimeWidget import SecondDateTimeWidget
from src.models.SessionWrapper import SessionWrapper


class UtilityForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("utility_page")
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.landing_layout = QHBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.landing_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def initUI(self):
        date_time_diff_section = QWidget()
        date_time_diff_section.setFixedWidth(600)
        date_time_diff_section.setFixedHeight(300)
        date_time_diff_label = RegularLabel("DateTime Difference : ")
        date_time_diff_layout = QVBoxLayout()
        first_date_time_line = QHBoxLayout()
        first_date_time_label = RegularLabel("From : ")
        self.first_date_time = DateTimeWidget(-1000, 600)
        first_date_time_line.addWidget(first_date_time_label)
        first_date_time_line.addWidget(self.first_date_time)

        second_date_time_line = QHBoxLayout()
        second_date_time_label = RegularLabel("To : ")
        self.second_date_time = SecondDateTimeWidget(-1000, 600)
        second_date_time_line.addWidget(second_date_time_label)
        second_date_time_line.addWidget(self.second_date_time)

        date_time_btn_line = QHBoxLayout()
        date_time_btn_line.setContentsMargins(500, 0, 0, 0)
        date_time_btn = RegularButton("Calculate")
        date_time_btn.clicked.connect(self.calculate_date_time_difference)
        date_time_btn_line.addWidget(date_time_btn)

        date_time_diff_layout.addWidget(date_time_diff_label)
        date_time_diff_layout.addLayout(first_date_time_line)
        date_time_diff_layout.addLayout(second_date_time_line)
        date_time_diff_layout.addLayout(date_time_btn_line)

        date_time_diff_section.setLayout(date_time_diff_layout)
        self.landing_layout.addWidget(date_time_diff_section)
        self.setLayout(self.landing_layout)
        # self.setS

    def calculate_date_time_difference(self):
        print('da')
        first_date_time = self.first_date_time.value()
        second_date_time = self.second_date_time.value()
        first_date_time_object = datetime.strptime(first_date_time, "%Y-%m-%d %H:%M:%S")
        second_date_time_object = datetime.strptime(second_date_time, "%Y-%m-%d %H:%M:%S")
        diff = second_date_time_object - first_date_time_object
        MessageBoxes.success_message("Result", "The difference is: "+str(diff.days))
