import sys
from PyQt5.QtCore import Qt, QEvent, QPoint
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QProxyStyle, QStyle, QApplication, QMainWindow, \
    QStackedWidget, QDialog, QScrollArea, QAction, QToolBar, QMenu
from src.Elements.MessageBoxes import MessageBoxes
from src.forms.aboutForm import About
from src.forms.landingForm import LandingForm
from src.forms.loginForm import Login
from src.Elements.ToolBar import ToolBar, MyQAction
############################################################
# Main App                                                 #
############################################################
from src.modals.createAccountModal import CreateAccountModal
from src.modals.newPasswordModal import NewPasswordModal
from src.models.AppFonts import RegularFont
from src.models.SessionWrapper import SessionWrapper


class Window(QMainWindow):
    def __init__(self, which='landing'):
        super().__init__()
        self.setFocusPolicy(Qt.TabFocus)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.central_widget = QStackedWidget()
        if which == 'landing':
            first_widget = LandingForm(self)
            self.setWindowTitle("Offline Docs / Home Page")
        else:
            first_widget = About(self, order=True)
            self.setWindowTitle("Offline Docs / About")
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

    # def closeEvent(self, event):
    #     confirm = MessageBoxes.confirm_message("close the app ?")
    #     if confirm:
    #         event.accept()
    #     else:
    #         event.ignore()

    # def eventFilter(self, object, event):
    #     if event.type() == QEvent.MouseButtonPress:
    #         if isinstance(object, MyQAction):
    #             print("Mouse pressed 1")
    #             pos = event.pos()
    #             parentPosition = self.mapToGlobal(QPoint(0, 0))
    #             menuPosition = parentPosition + pos
    #             self.images_menu.move(menuPosition)
    #             self.images_menu.show()
    #             return True
    #         else:
    #             print(type(object))
    #     return False


############################################################
# Create a custom "QProxyStyle" to enlarge the QMenu icons #
############################################################
class MyProxyStyle(QProxyStyle):
    pass

    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):
        if QStyle_PixelMetric == QStyle.PM_ToolBarIconSize:
            return 40
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


############################################################
# instantiate the app with login dialog                    #
############################################################

### pyinstaller :: pyinstaller --onefile --windowed --icon=resources\assets\images\icon.ico medicBook.py

def run_app():
    app = QApplication(sys.argv)
    # app.setLayoutDirection(Qt.RightToLeft)
    app.setApplicationName("Offline Docs")
    app.setWindowIcon(QIcon('resources/assets/images/logo.png'))
    app_font = RegularFont()
    app.setFont(app_font)
    myStyle = MyProxyStyle('Fusion')
    app.setStyle(myStyle)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    # print('Available: %dx%d' % (rect.width(), rect.height()))
    SessionWrapper.screen_dim = ('%dx%d' % (rect.width(), rect.height()))
    SessionWrapper.screen_width = rect.width()
    SessionWrapper.screen_height = rect.height()
    # print('Screen: %s' % screen.name())
    # size = screen.size()
    # print('Size: %d x %d' % (size.width(), size.height()))

    css_file = "resources/assets/css/style.qss"
    app.setStyleSheet(open(css_file, "r").read())
    login = Login()
    ############################################################
    # if login succeed start the main page                     #
    ############################################################
    login_result = login.exec_()
    if login_result == QDialog.Accepted and login.status == "Done" and not login.do_order:
        window = Window()
        # window.showMaximized()
        window.show()
        sys.exit(app.exec_())
    elif login_result == QDialog.Accepted and login.status == "New":
        new_password = NewPasswordModal()
        login_result = login.exec_()
        if login_result == QDialog.Accepted and new_password.status == "Done":
            window = Window()
            # window.showMaximized()
            window.show()
            sys.exit(app.exec_())
    elif login_result == QDialog.Accepted and login.status == "register":
        registration_modal = CreateAccountModal()
        login_result = login.exec_()
        if login_result == QDialog.Accepted and registration_modal.status == "Done":
            window = Window()
            window.showMaximized()
            sys.exit(app.exec_())
    elif login_result == QDialog.Accepted and login.status == "expired":
        if login.do_order:
            window = Window('do_order')
            window.showMaximized()
            sys.exit(app.exec_())
        else:
            app.quit()
    elif login_result == QDialog.Accepted and login.do_order:
        window = Window('do_order')
        window.showMaximized()
        sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
