from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFrame

from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.ClickableLabel import ClickableLabel, ActiveLabel
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
        self.setObjectName("category_page")
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
        categories_tab = ActiveLabel("Categories")
        documents_tab = ClickableLabel("Documents")
        self.landing_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        self.landing_layout.addWidget(categories_tab)
        self.landing_layout.addWidget(documents_tab)
        self.setLayout(self.landing_layout)
        # self.setS
