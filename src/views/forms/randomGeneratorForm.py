import string
import random

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox

from src.views.Widgets.CustomLabel import RegularLabel
from src.views.Widgets.LabeledTextArea import LabeledTextArea
from src.views.Widgets.MessageBoxes import MessageBoxes
from src.views.Widgets.RegularButton import RegularButton
from src.views.Widgets.RegularTextBox import RegularTextBox
from src.models.SessionWrapper import SessionWrapper


class RandomGeneratorForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("my_calendar_page")
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.landing_layout = QHBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.landing_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

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
        self.random_length_select = RegularTextBox(text=10)
        self.random_length_select.setValidator(QIntValidator())

        self.random_length_select.setFixedWidth(60)

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

    def generate_random(self):
        if not len(self.random_length_select.text()):
            MessageBoxes.warning_message("Error", "choose the length please !")
            return
        string_length = int(self.random_length_select.text())
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

    def initUI(self):
        # lbl = RegularLabel("This will be My Calendar page")
        # self.landing_layout.addWidget(lbl)
        # self.setLayout(self.landing_layout)
        random_string_section = self.make_random_string_section()
        self.landing_layout.addWidget(random_string_section)
        self.setLayout(self.landing_layout)
