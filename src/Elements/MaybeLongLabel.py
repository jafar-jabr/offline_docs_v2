from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.Elements.CustomLabel import RegularLabel
from src.modals.fullTextModal import FullTextModal
from src.models.SharedFunctions import SharedFunctions


class IconicQLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        pixmap = QPixmap('resources/assets/images/see_more.png')
        pixmap_resized1 = pixmap.scaled(25, 25, Qt.KeepAspectRatio)
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

    def mousePressEvent(self, ev):
        self.clicked.emit()


class MaybeLongLabel(QWidget):
    def __init__(self, text, title, limit=100):
        super().__init__()
        self.limit = limit
        self.the_title = title
        text = str(text)
        self.text = text
        full_text = text.strip()
        short_text = SharedFunctions.format_text(full_text, self.limit, True)
        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.the_label = RegularLabel(short_text)
        self.main_layout.addWidget(self.the_label)
        if len(full_text) > limit:
            self.icon_label = IconicQLabel()
            self.icon_label.clicked.connect(self.show_full_text)
            self.main_layout.addWidget(self.icon_label)
        self.setLayout(self.main_layout)
        self.setLayoutDirection(Qt.RightToLeft)

    def value(self):
        return 12

    def setText(self, text):
        text = str(text)
        self.text = text
        full_text = text.strip()
        short_text = SharedFunctions.format_text(full_text, self.limit, True)
        self.the_label.setText(short_text)

        if len(full_text) > self.limit:
            try:
                p = QPixmap('resources/assets/images/see_more.png')
                self.icon_label.setPixmap(p)
            except AttributeError:
                self.icon_label = IconicQLabel()
                self.icon_label.clicked.connect(self.show_full_text)
                self.main_layout.addWidget(self.icon_label)
        else:
            try:
                p = QPixmap()
                self.icon_label.setPixmap(p)
            except AttributeError:
                pass

    def show_full_text(self):
        FullTextModal(self.the_title, self.text)
