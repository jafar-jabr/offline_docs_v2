from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem

from src.Elements.ClickableLabel import ClickableLabel
from src.Elements.CustomLabel import HeadLineLabel
from src.Elements.FilterTextBox import FilterTextBox
from src.Elements.LabeledTextArea import LabeledTextArea
from src.Elements.LabeledTextBox import LabeledTextBox
from src.Elements.RegularTextBox import RegularTextBox
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
        self.landing_layout = QHBoxLayout()
        self.landing_layout.setContentsMargins(20, 20, 20, 50) #(left, top, right, bottom)
        self.landing_layout.setSpacing(20)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def initUI(self):
        lef_column = QVBoxLayout()
        lef_column.setContentsMargins(20, 20, 20, 50)  # (left, top, right, bottom)
        search_input = FilterTextBox(260, False, "resources/assets/images/search.png", "Search")
        lef_column.addWidget(search_input)
        tabs_line = QHBoxLayout()
        categories_tab = ClickableLabel("Categories")
        documents_tab = ClickableLabel("Documents")

        tabs_line.addWidget(categories_tab)
        tabs_line.addWidget(documents_tab)
        lef_column.addLayout(tabs_line)

        categories_list = QListWidget()
        categories_list.setFixedWidth(260)
        categories_list.installEventFilter(self)
        for opt in ['a', 'b', 'c', 'd']:
            item = QListWidgetItem(opt)
            categories_list.addItem(item)
        lef_column.addWidget(categories_list)
        right_column = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setFixedWidth(800)
        right_content = QVBoxLayout()
        category_name = LabeledTextBox("Category Name: ", width=500)
        category_desc = LabeledTextArea("Description: ", height=200, space=25, width=500)
        right_content.addWidget(category_name)
        right_content.addWidget(category_desc)
        right_widget.setLayout(right_content)
        right_column.addWidget(right_widget)
        self.landing_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        right_content.setContentsMargins(0, 100, 0, 0)  # (left, top, right, bottom)
        self.landing_layout.addLayout(lef_column)
        self.landing_layout.addLayout(right_column)
        self.setLayout(self.landing_layout)
        # self.setS
