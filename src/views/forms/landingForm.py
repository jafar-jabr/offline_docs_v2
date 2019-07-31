from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from src.views.widgets.ClickableIcon import ClickableIcon
from src.models.DatabaseModel import Database
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, \
    QStackedWidget, QDialog, QScrollArea
from src.views.widgets.ToolBar import ToolBar
############################################################
# Main App                                                 #
############################################################
from src.models.AppFonts import RegularFont
from src.models.SessionWrapper import SessionWrapper


class MainWindow(QMainWindow):
    current_instance = None

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setFocusPolicy(Qt.TabFocus)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        self.central_widget = QStackedWidget()

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

        self.setObjectName("main_window")
        self.setFixedWidth(1200)
        self.setFixedHeight(800)
        self.show()

    def run(self, which):
        self.central_widget.addWidget(which)
        self.central_widget.setCurrentWidget(which)
        if not self.current_instance:
            self.current_instance = self


class LandingForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        window_width = SessionWrapper.get_dimension('login_width')
        window_height = SessionWrapper.get_dimension('login_height')
        app_font = RegularFont()
        self.setFont(app_font)
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("landing_page")
        the_layout = QVBoxLayout()

        destinations_line = QHBoxLayout()
        destinations_line.setSpacing(80)
        destinations_line.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)

        offline_docs_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/offline-doc.png', tool_tip="Offline documentation")
        offline_docs_btn.clicked.connect(lambda: self.go_to_form('categories'))
        destinations_line.addWidget(offline_docs_btn)

        sticky_notes_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/sticky.png', tool_tip="Sticky notes")
        sticky_notes_btn.clicked.connect(lambda: self.go_to_form('sticky_notes'))
        destinations_line.addWidget(sticky_notes_btn)

        calendar_btn = ClickableIcon(100, 100, 'resources/assets/images/Landing/calendar.png', tool_tip="Calendar")
        calendar_btn.clicked.connect(lambda: self.go_to_form('my_calendar'))
        destinations_line.addWidget(calendar_btn)
        the_layout.addLayout(destinations_line)

        second_line = QHBoxLayout()
        second_line.setSpacing(80)
        second_line.setContentsMargins(30, 0, 30, 0)  # (left, top, right, bottom)

        time_diff_btn = ClickableIcon(80, 80, 'resources/assets/images/Landing/date-time-difference.png',
                                         tool_tip="Date Time Difference")
        time_diff_btn.clicked.connect(lambda: self.go_to_form('date_time_difference'))
        second_line.addWidget(time_diff_btn)

        random_gen_btn = ClickableIcon(80, 80, 'resources/assets/images/Landing/random-string-generator.png',
                                         tool_tip="Random generator")
        random_gen_btn.clicked.connect(lambda: self.go_to_form('random_generator'))
        second_line.addWidget(random_gen_btn)

        qr_code_btn = ClickableIcon(80, 80, 'resources/assets/images/Landing/qr-code-generator.png',
                                     tool_tip="QR Code generator")
        qr_code_btn.clicked.connect(lambda: self.go_to_form('qr_generator'))
        second_line.addWidget(qr_code_btn)

        the_layout.addLayout(second_line)

        # self.resize(502, 261)
        self.setFixedSize(800, 500)
        self.setWindowTitle("Offline Docs / Main Page")
        self.setLayout(the_layout)

    def go_to_form(self, which, **kwargs):
        self.accept()
        from src.models.PlayMouth import PlayMouth
        page = PlayMouth.all_pages(which)
        main_window = MainWindow.current_instance
        if not main_window:
            main_window = MainWindow()
        main_window.run(page(main_window, **kwargs))

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

