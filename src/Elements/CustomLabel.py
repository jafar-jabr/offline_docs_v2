from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLabel

from src.models.SessionWrapper import SessionWrapper


class CustomLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        # self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
               QLabel{
                   color: %s;
                   font-size: %s;
                   margin: 0 10px;
               }
               """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.setStyleSheet(style)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class RegularLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        style = """
               QLabel{
                   color: %s;
                   font-size: %s;
                   margin: 0 10px;
               }
               """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.setStyleSheet(style)

    def setWidth(self, w):
        self.setGeometry(QRect(self.x(), self.y(), w, self.height()))


class HeadLineLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if 'color' in kwargs:
            color = kwargs['color'],
        else:
            color = "rgb(250, 250, 250)",
        style = """
               QLabel{
                   color: %s;
                   font-size: %s;
                   margin: 0 10px;
               }
               """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.big_size])
        self.setStyleSheet(style)


class UrlLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        if 'color' in kwargs:
            color = kwargs['color'],
        else:
            color = "rgb(250, 250, 250)",
        style = """
               QLabel{
                   color: %s;
                   font-size: %s;
                   margin: 0 10px;
               }
               """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.big_size])
        self.setStyleSheet(style)


class MidSizeLabel(QLabel):

    def __init__(self, *args):
        super().__init__(*args)
        style = """
               QLabel{
                   color: %s;
                   font-size: %s;
                   margin: 0 10px;
               }
               """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.setStyleSheet(style)
