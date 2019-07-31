from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QPushButton
from src.views.Widgets.ClickableLineEdit import ClickableLineEdit


class PathSelector(QWidget):
    selected_path = ""

    def __init__(self, max_w=240, start_path=''):
        super().__init__()
        self.start_path = start_path
        self.the_line = QHBoxLayout()
        PathSelector.selected_path = start_path
        self.the_line.setContentsMargins(0, 0, 0, 0)
        self.the_line.setSpacing(0)
        self.text = ClickableLineEdit()
        self.text.setFixedHeight(33)
        self.setMaximumWidth(max_w)
        self.text.setText("           "+start_path)
        self.text.setReadOnly(True)
        self.text.clicked.connect(self.do_select_path)
        self.text.setAlignment(Qt.AlignRight)
        self.text.setStyleSheet("border-top-right-radius: 10px; border-bottom-right-radius: 10px; padding: 7px;")
        self.button = QPushButton()
        pixmap = QIcon("resources/assets/images/upload-blue.png")
        self.button.setIcon(pixmap)
        self.button.setIconSize(QSize(33, 33))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; background-color : #fff;")
        self.the_line.addWidget(self.text)
        self.the_line.addWidget(self.button)
        self.button.clicked.connect(self.do_select_path)
        self.setLayout(self.the_line)

    def do_select_path(self):
        options = QFileDialog.Options()
        the_path = str(QFileDialog.getExistingDirectory(None, "اختر مسار الحفظ", self.start_path, options=options))
        if the_path:
            PathSelector.selected_path = the_path
            self.text.setText(the_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass
        else:
            super().mousePressEvent(event)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)

    def setText(self, txt):
        self.text.setText(txt)

    @staticmethod
    def value():
        return PathSelector.selected_path
