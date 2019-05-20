from PyQt5.QtWidgets import QHBoxLayout, QWidget

from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.MessageBoxes import MessageBoxes
from src.forms.categoryForm import CategoryForm
from src.forms.myCalendarForm import MyCalendarForm
from src.forms.stickyNotesForm import StickyNotesForm
from src.forms.dateTimeDifferenceForm import DateTimeDifferenceForm
from src.forms.qrGeneratorForm import QrCodeGenerator
from src.forms.randomGeneratorForm import RandomGeneratorForm
# from src.forms.utilityForm import UtilityForm
# from src.forms.utilityLandingForm import UtilityLandingPage
from src.models.DatabaseModel import Database
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, \
    QStackedWidget, QDialog, QScrollArea, QAction, QMenu
from src.forms.aboutForm import About
from src.Elements.ToolBar import ToolBar
############################################################
# Main App                                                 #
############################################################
from src.models.AppFonts import RegularFont
from src.models.SessionWrapper import SessionWrapper


class UtilityLandingForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        window_width = SessionWrapper.get_dimension('login_width')
        window_height = SessionWrapper.get_dimension('login_height')
        app_font = RegularFont()
        self.setFont(app_font)
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("utilities_landing_page")

        destinations_line = QHBoxLayout()
        destinations_line.setSpacing(80)
        destinations_line.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)

        offline_docs_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/date-time-difference.png', tool_tip="Date Time Difference")
        offline_docs_btn.clicked.connect(lambda: self.go_to_page('date_time_difference'))
        # offline_docs_btn.clicked.connect((lambda: self.go_to_page('categories')))
        destinations_line.addWidget(offline_docs_btn)

        sticky_notes_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/random-string-generator.png', tool_tip="Random generator")
        sticky_notes_btn.clicked.connect(lambda: self.go_to_page('random_generator'))
        destinations_line.addWidget(sticky_notes_btn)

        calendar_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/qr-code-generator.png', tool_tip="QR Code generator")
        calendar_btn.clicked.connect(lambda: self.go_to_page('qr_generator'))
        destinations_line.addWidget(calendar_btn)

        # utility_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/date-time.png', tool_tip="Date/time convert")
        # utility_btn.clicked.connect(lambda: self.go_to_form('utility'))
        # destinations_line.addWidget(utility_btn)

        # self.resize(502, 261)
        self.setFixedSize(800, 500)
        self.setWindowTitle("Offline Docs / Main Page")
        self.setLayout(destinations_line)

    def go_to_page(self, which):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to(which)

    def get_preferences(self, user_id):
        pref = Database().get_preferences(user_id)
        SessionWrapper.font_color = pref['font_color']
        SessionWrapper.regular_size = pref['regular_size']
        SessionWrapper.big_size = pref['big_size']
        SessionWrapper.app_mode = pref['app_mode']
        SessionWrapper.main_doctor_id = pref['main_doctor_id']

    def closeEvent(self, event):
        sys.exit()
        # event.accept()

    def show(self):
        self.exec_()
