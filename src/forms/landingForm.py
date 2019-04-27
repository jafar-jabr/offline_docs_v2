from PyQt5.QtWidgets import QHBoxLayout

from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.MessageBoxes import MessageBoxes
from src.forms.categoryForm import CategoryForm
from src.forms.myCalendarForm import MyCalendarForm
from src.forms.stickyNotesForm import StickyNotesForm
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


class MainWindow(QMainWindow):
    def __init__(self, which):
        super().__init__()
        self.setFocusPolicy(Qt.TabFocus)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        self.central_widget = QStackedWidget()
        if which == 'landing':
            first_widget = CategoryForm(self)
            self.setWindowTitle("Offline Docs / Home Page")
        elif which == "sticky_notes":
            first_widget = StickyNotesForm(self)
            self.setWindowTitle("Offline Docs / Sticky Notes")
        elif which == "my_calendar":
            first_widget = MyCalendarForm(self)
            self.setWindowTitle("Offline Docs / My Calendar")
        else:
            first_widget = CategoryForm(self)
            self.setWindowTitle("Offline Docs / Home Page")
        self.central_widget.addWidget(first_widget)
        scroll.setWidget(self.central_widget)
        self.setCentralWidget(scroll)
        self.toolbar = self.addToolBar('&Main')
        self.toolbar.setLayoutDirection(Qt.RightToLeft)
        self.toolbar.toggleViewAction().setEnabled(False)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.toolbar.addActions(btn for btn in ToolBar(self).Buttons)
        self.statusBar().showMessage("Offline Documentation is your external memory")
        self.toolbar.installEventFilter(self)
        self.installEventFilter(self)

        self.images_menu = QMenu()
        opt = ['معاينة', 'تحديث', 'حذف']
        for i in opt:
            actn = QAction(QIcon('resources/assets/images/drop_down_h.png'), i, self.images_menu)
            actn.setObjectName(i)
            # actn.triggered.connect(self.menu_clicked)
            self.images_menu.addAction(actn)

        self.setObjectName("main_window")
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        # p = self.mapToGlobal(QPoint(0, 0))
        # print(p)
        # self.move(p)
        self.show()


class LandingForm(QDialog):
    def __init__(self):
        super().__init__()
        window_width = SessionWrapper.get_dimension('login_width')
        window_height = SessionWrapper.get_dimension('login_height')
        app_font = RegularFont()
        self.setFont(app_font)
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("login")

        destinations_line = QHBoxLayout()
        destinations_line.setSpacing(80)
        destinations_line.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)

        offline_docs_btn = ClickableIcon(100, 100, 'resources/assets/images/logo.png')
        offline_docs_btn.clicked.connect(lambda: self.go_to_form('landing'))
        destinations_line.addWidget(offline_docs_btn)

        sticky_notes_btn = ClickableIcon(100, 100, 'resources/assets/images/logo.png')
        sticky_notes_btn.clicked.connect(lambda: self.go_to_form('sticky_notes'))
        destinations_line.addWidget(sticky_notes_btn)

        calendar_btn = ClickableIcon(100, 100, 'resources/assets/images/logo.png')
        calendar_btn.clicked.connect(lambda: self.go_to_form('my_calendar'))
        destinations_line.addWidget(calendar_btn)

        # self.resize(502, 261)
        self.setFixedSize(800, 500)
        self.setWindowTitle("Offline Docs / Main Page")
        self.setLayout(destinations_line)

    def go_to_form(self, which):
        self.accept()
        MainWindow(which)
        # sys.exit(self.app.exec_())

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
