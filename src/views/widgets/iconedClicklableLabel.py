from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from src.views.widgets.ClickableLineEdit import ClickableLineEdit


class IconedClickableLabel(QWidget):
    clicked = pyqtSignal()

    def __init__(self, txt, max_w=240):
        super().__init__()
        # ImageSelector.image_url = ""
        self.the_line = QHBoxLayout()
        self.the_line.setContentsMargins(0, 0, 0, 0)
        self.the_line.setSpacing(0)
        self.text = ClickableLineEdit()
        self.text.setFixedHeight(33)
        self.setMaximumWidth(max_w)
        self.text.setText(txt)
        self.text.setReadOnly(True)
        self.text.clicked.connect(self.emit_clicked)
        self.text.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; padding: 7px;")
        self.img_select_btn = QPushButton()
        self.img_select_btn.setAutoDefault(False)
        pixmap = QIcon("resources/assets/images/import.png")
        self.img_select_btn.setIcon(pixmap)
        self.img_select_btn.setIconSize(QSize(33, 33))
        self.img_select_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.text.setCursor(QCursor(Qt.PointingHandCursor))
        self.img_select_btn.setStyleSheet("border-top-right-radius: 10px; border-bottom-right-radius: 10px; background-color : #fff;")
        self.the_line.addWidget(self.text)
        self.the_line.addWidget(self.img_select_btn)
        self.img_select_btn.clicked.connect(self.emit_clicked)
        self.setLayout(self.the_line)

    def emit_clicked(self):
        self.clicked.emit()

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)

    def setText(self, txt):
        self.text.setText(txt)
