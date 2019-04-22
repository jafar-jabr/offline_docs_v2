from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel
from src.models.SessionWrapper import SessionWrapper


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
                       QLabel{
                           color: #fff;
                           font-size: %s;
                           margin: 0 10px;
                           background-color: #445566;
                       }
                       """ % SessionWrapper.number_to_size[SessionWrapper.regular_size]
        self.setStyleSheet(style)
        self.setMaximumHeight(45)
        # self.fixWidth()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.rightClicked.emit()

    def fixWidth(self):
        length = len(self.text())
        if length > 2:
            self.setFixedWidth(int(length*9.5))


class ActiveLabel(QLabel):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
                       QLabel{
                           color: #fff;
                           font-size: %s;
                           padding: 10px;
                           background-color: #445559;
                       }
                       """ % (SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.setStyleSheet(style)
        self.setMaximumHeight(45)
        # self.fixWidth()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.rightClicked.emit()

    def fixWidth(self):
        length = len(self.text())
        if length > 2:
            self.setFixedWidth(int(length*9.5))


class ForgotPasswordLabel(QLabel):
    clicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
                       QLabel{
                           color: %s;
                           font-size: %s;
                           margin: 0 10px;
                           text-decoration: underline;
                       }
                       """ % (SessionWrapper.font_color, '16px')
        self.setStyleSheet(style)
        self.setMaximumHeight(45)
        self.fixWidth()

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        elif ev.button() == Qt.RightButton:
            self.rightClicked.emit()

    def fixWidth(self):
        length = len(self.text())
        if length > 2:
            self.setFixedWidth(int(length*9.5))
