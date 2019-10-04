from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QLabel
from PyQt5.QtCore import QThread, QObject, pyqtSignal, Qt

from src.models.EmailSenderLight import EmailSender


class IconicQLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.resize(100, 100)
        pixmap = QMovie('resources/assets/images/loading-small.gif')
        pixmap.setScaledSize(self.size())
        self.setMovie(pixmap)
        self.setCursor(QCursor(Qt.WaitCursor))
        pixmap.start()


class Spinner(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        la = QHBoxLayout()
        ll = IconicQLabel()
        la.addWidget(ll)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        self.setLayout(la)

    def start(self):
        self.exec_()


class MyThread(QThread):
    """
    This class is not required if you're using the builtin
    version of threading.
    """
    def __init__(self):
        super().__init__()

    def run(self):
        """This overrides a default run function."""
        self.quit()


class HandleLongProcess:

    def do_sending(self, subject, body):
        try:
            self.my_loader = Spinner()
            self.socketController = LongProcess(self.my_loader, subject, body)
            self.simulThread = MyThread()
            self.socketController.moveToThread(self.simulThread)
            self.simulThread.start()
            self.simulThread.started.connect(self.socketController.do_the_job)
            self.my_loader.start()
            self.socketController.finished.connect(self.long_process_done)
            return 'Sent'
        except:
            return 'error'

    def long_process_done(self):
        self.my_loader.hide()
        self.my_loader.accept()
        self.simulThread.quit()


class LongProcess(QObject):
    finished = pyqtSignal()

    def __init__(self, loader, subject, body):
        super().__init__()
        self.my_loader = loader
        self.subject = subject
        self.msg_body = body

    def do_the_job(self):
        # setup the socket
        EmailSender.send_html_email(self.subject, self.msg_body)
        self.finished.emit()
        self.my_loader.hide()
        self.my_loader.accept()



