import string
import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, QCheckBox, QComboBox
from src.Elements.CustomLabel import RegularLabel
from datetime import datetime, timedelta
from src.Elements.LabeledTextArea import LabeledTextArea
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.dateTimeWidget import DateTimeWidget
from src.Elements.secondDateTimeWidget import SecondDateTimeWidget
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class UtilityForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("utility_page")
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.landing_layout = QVBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 0, 100) #(left, top, right, bottom)
        self.landing_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.result_type = "In Details"
        self.initUI()

    def initUI(self):
        date_time_diff_section = self.make_date_time_section()
        random_string_section = self.make_random_string_section()
        self.landing_layout.addWidget(date_time_diff_section)
        self.landing_layout.addWidget(random_string_section)
        self.setLayout(self.landing_layout)
        # self.setS

    def make_date_time_section(self):
        date_time_diff_section = QWidget()
        date_time_diff_section.setFixedWidth(550)
        date_time_diff_section.setFixedHeight(300)
        date_time_diff_label = RegularLabel("DateTime Difference : ")
        date_time_diff_layout = QVBoxLayout()
        first_date_time_line = QHBoxLayout()
        first_date_time_label = RegularLabel("From : ")
        self.first_date_time = DateTimeWidget(-600, 600)
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

    def make_random_string_section(self):
        random_string_section = QWidget()
        random_string_section.setFixedWidth(550)
        random_string_section.setFixedHeight(300)
        random_string_label = RegularLabel("Random Generator : ")
        random_string_layout = QVBoxLayout()

        random_options_line = QHBoxLayout()

        self.capital_etters = QCheckBox("Capital Letters")
        self.capital_etters.setChecked(True)
        self.small_letters = QCheckBox("Small Letters")
        self.numbers = QCheckBox("Numbers")
        self.special_characters = QCheckBox("Special Characters")

        random_options_line.addWidget(self.capital_etters)
        random_options_line.addWidget(self.small_letters)
        random_options_line.addWidget(self.numbers)
        random_options_line.addWidget(self.special_characters)

        random_length_line = QHBoxLayout()
        random_length_line.setContentsMargins(0, 0, 360, 0)  # (left, top, right, bottom)
        random_length_label = RegularLabel("Length : ")
        random_length_label.setWidth(120)
        self.random_length_select = QComboBox()
        self.random_length_select.setFixedWidth(60)
        for option in range(1, 501):
            self.random_length_select.addItem(str(option))

        random_length_line.addWidget(random_length_label)
        random_length_line.addWidget(self.random_length_select)
        self.random_string = LabeledTextArea("Random String: ", height=200, space=25, width=550)

        random_string_btn_line = QHBoxLayout()
        random_string_btn_line.setContentsMargins(450, 0, 0, 0)
        date_time_btn = RegularButton("Generate")
        date_time_btn.clicked.connect(self.generate_random)
        random_string_btn_line.addWidget(date_time_btn)

        random_string_layout.addWidget(random_string_label)
        random_string_layout.addLayout(random_options_line)
        random_string_layout.addLayout(random_length_line)
        random_string_layout.addLayout(random_string_btn_line)
        random_string_layout.addWidget(self.random_string)

        random_string_section.setLayout(random_string_layout)
        return random_string_section

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

    def generate_random(self):
        string_length = int(self.random_length_select.currentText())
        letters = ''
        if self.capital_etters.isChecked():
            letters += string.ascii_uppercase
        if self.small_letters.isChecked():
            letters += string.ascii_lowercase
        if self.numbers.isChecked():
            letters += string.digits
        if self.special_characters.isChecked():
            letters += string.punctuation
        if len(letters) == 0:
            MessageBoxes.warning_message("Error", "you have to choose one group at least !")
            return
        randd = ''.join(random.choice(letters) for i in range(string_length))
        self.random_string.setText(randd)


# if __name__ == '__main__':
#     rand = UtilityForm.generate_random(8)
#     print(rand)
