import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QProxyStyle, QStyle, QApplication, QDialog
from src.forms.landingForm import LandingForm
from src.forms.loginForm import Login
############################################################
# Main App                                                 #
############################################################
from src.modals.createAccountModal import CreateAccountModal
from src.modals.newPasswordModal import NewPasswordModal
from src.models.AppFonts import RegularFont
from src.models.SessionWrapper import SessionWrapper




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
    app.setApplicationName("Offline Docs")
    app.setWindowIcon(QIcon('resources/assets/images/logo.png'))
    app_font = RegularFont()
    app.setFont(app_font)
    myStyle = MyProxyStyle('Fusion')
    app.setStyle(myStyle)
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    screen_center = screen.availableGeometry().center()
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
        window = LandingForm()
        window.show()
        sys.exit(app.exec_())
    elif login_result == QDialog.Accepted and login.status == "New":
        new_password = NewPasswordModal()
        login_result = login.exec_()
        if login_result == QDialog.Accepted and new_password.status == "Done":
            window = LandingForm()
            window.show()
    elif login_result == QDialog.Accepted and login.status == "register":
        registration_modal = CreateAccountModal()
        if login_result == QDialog.Accepted and registration_modal.status == "Done":
            window = LandingForm()
            window.show()
    elif login_result == QDialog.Accepted and login.status == "expired":
        if login.do_order:
            window = LandingForm()
            window.show()
        else:
            app.quit()
    elif login_result == QDialog.Accepted and login.do_order:
        window = LandingForm()
        window.show()


if __name__ == '__main__':
    run_app()
