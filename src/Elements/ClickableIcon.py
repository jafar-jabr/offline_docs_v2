from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QLabel


class ClickableIcon(QLabel):
    clicked = pyqtSignal()

    def __init__(self, w, h, url='resources/assets/images/pdf.png', tool_tip=""):
        super().__init__()
        self.setToolTip(tool_tip)
        pixmap = QPixmap(url)
        pixmap_resized1 = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        self.setPixmap(pixmap_resized1)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # style = """
        #        QLabel:hover {
        #            background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 cyan, stop:1 #2A5058);
        #            border-style: outset;
        #            border-width: 2px;
        #            border-radius: 15px;
        #            border-color: green;
        #            padding: 4px;
        #        }
        #
        #        """
        # self.setStyleSheet(style)
        self.setMaximumWidth(w)
        self.setMaximumHeight(h)

    def mousePressEvent(self, ev):
        self.clicked.emit()

