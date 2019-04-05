from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QPushButton


class RegularButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
        QPushButton {
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: #ffffff;
            padding: 7px;
            background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 cyan, stop:1 #61a2b1);
        }
        QPushButton:hover {
            background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 cyan, stop:1 #2A5058);
            border-style: outset;
            border-width: 2px;
            border-radius: 15px;
            border-color: green;
            padding: 4px;
        }

        """
        self.setStyleSheet(style)

