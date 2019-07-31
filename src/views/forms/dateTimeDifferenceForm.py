from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton
from src.views.Widgets.CustomLabel import RegularLabel
from datetime import datetime
from src.views.Widgets.MessageBoxes import MessageBoxes
from src.views.Widgets.RegularButton import RegularButton
from src.views.Widgets.dateTimeWidget import DateTimeWidget
from src.views.Widgets.secondDateTimeWidget import SecondDateTimeWidget
from src.models.SessionWrapper import SessionWrapper
from src.models.GenericFunctions import SharedFunctions


class DateTimeDifferenceForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("my_calendar_page")
        self.result_type = "In Details"
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.landing_layout = QHBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.landing_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def make_date_time_section(self):
        date_time_diff_section = QWidget()
        date_time_diff_section.setFixedWidth(550)
        date_time_diff_section.setFixedHeight(300)
        date_time_diff_label = RegularLabel("DateTime Difference : ")
        date_time_diff_layout = QVBoxLayout()
        first_date_time_line = QHBoxLayout()
        first_date_time_label = RegularLabel("From : ")
        yesterday = SharedFunctions.get_yesterday_date_str()
        self.first_date_time = DateTimeWidget(-600, 600, value=yesterday)
        first_date_time_line.addWidget(first_date_time_label)
        first_date_time_line.addWidget(self.first_date_time)

        second_date_time_line = QHBoxLayout()
        second_date_time_label = RegularLabel("To : ")
        self.second_date_time = SecondDateTimeWidget(-600, 600)
        second_date_time_line.addWidget(second_date_time_label)
        second_date_time_line.addWidget(self.second_date_time)

        calculation_options_line = QHBoxLayout()

        self.calculation_options_group = QButtonGroup()  # Number group

        r1 = QRadioButton("In Details")
        r1.setChecked(True)
        r1.toggled.connect(lambda: self.set_result_type(r1, "In Details"))
        r2 = QRadioButton("In Days")
        r2.toggled.connect(lambda: self.set_result_type(r2, "In Days"))
        r3 = QRadioButton("In Hours")
        r3.toggled.connect(lambda: self.set_result_type(r3, "In Hours"))
        r4 = QRadioButton("In Minutes")
        r4.toggled.connect(lambda: self.set_result_type(r4, "In Minutes"))
        r5 = QRadioButton("In Seconds")
        r5.toggled.connect(lambda: self.set_result_type(r5, "In Seconds"))

        self.calculation_options_group.addButton(r1)
        self.calculation_options_group.addButton(r2)
        self.calculation_options_group.addButton(r3)
        self.calculation_options_group.addButton(r4)
        self.calculation_options_group.addButton(r5)

        calculation_options_line.addWidget(r1)
        calculation_options_line.addWidget(r2)
        calculation_options_line.addWidget(r3)
        calculation_options_line.addWidget(r4)
        calculation_options_line.addWidget(r5)

        date_time_btn_line = QHBoxLayout()
        date_time_btn_line.setContentsMargins(450, 0, 0, 0)
        date_time_btn = RegularButton("Calculate")
        date_time_btn.clicked.connect(self.calculate_date_time_difference)
        date_time_btn_line.addWidget(date_time_btn)

        date_time_diff_layout.addWidget(date_time_diff_label)
        date_time_diff_layout.addLayout(first_date_time_line)
        date_time_diff_layout.addLayout(second_date_time_line)
        date_time_diff_layout.addLayout(calculation_options_line)
        date_time_diff_layout.addLayout(date_time_btn_line)

        date_time_diff_section.setLayout(date_time_diff_layout)
        return date_time_diff_section

    def calculate_date_time_difference(self):
        first_date_time = self.first_date_time.value()
        second_date_time = self.second_date_time.value()
        try:
            first_date_time_object = datetime.strptime(first_date_time, "%Y-%m-%d %H:%M:%S")
            second_date_time_object = datetime.strptime(second_date_time, "%Y-%m-%d %H:%M:%S")
            if first_date_time_object > second_date_time_object:
                MessageBoxes.warning_message("Error", "Start Time can not be after End Time !")
                return
        except ValueError as e:
            MessageBoxes.warning_message("Error", "Incorrect Date format ! " + str(e))
            return
        if self.result_type == "In Details":
            other_diff = SharedFunctions.date_diff(first_date_time_object, second_date_time_object)
        elif self.result_type == "In Days":
            other_diff = SharedFunctions.date_diff_days(first_date_time_object, second_date_time_object)
        elif self.result_type == "In Hours":
            other_diff = SharedFunctions.date_diff_hours(first_date_time_object, second_date_time_object)
        elif self.result_type == "In Minutes":
            other_diff = SharedFunctions.date_diff_minutes(first_date_time_object, second_date_time_object)
        elif self.result_type == "In Seconds":
            other_diff = SharedFunctions.date_diff_seconds(first_date_time_object, second_date_time_object)
        else:
            other_diff = SharedFunctions.date_diff(first_date_time_object, second_date_time_object)
        MessageBoxes.success_message("Result", "The difference is: "+str(other_diff))

    def set_result_type(self, instance, result_type):
        if instance.isChecked():
            self.result_type = result_type

    def initUI(self):
        # lbl = RegularLabel("This will be My Calendar page")
        # self.landing_layout.addWidget(lbl)

        date_time_diff_section = self.make_date_time_section()
        self.landing_layout.addWidget(date_time_diff_section)
        self.setLayout(self.landing_layout)

