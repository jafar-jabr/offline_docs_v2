from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget
from src.Elements.ClickableLineEdit import ClickableLineEdit


class IconTextBoxAR(QWidget):
    text_value = ""
    iconClicked = pyqtSignal()

    def __init__(self, is_read_only=False, icon="resources/assets/images/search.png", place_holder=None):
        super().__init__()
        self.the_line = QHBoxLayout()
        self.the_line.setSpacing(0)
        self.text_input = ClickableLineEdit()
        self.text_input.setFixedHeight(33)
        self.text_input.textChanged[str].connect(self.update_value)
        self.text_input.returnPressed.connect(self.event_emittor)
        if is_read_only:
            self.text_input.setReadOnly(True)
            self.text_input.clicked.connect(self.event_emittor)
        if place_holder:
            self.text_input.setPlaceholderText(place_holder)
        self.text_input.setAlignment(Qt.AlignRight)
        self.text_input.setStyleSheet("border-top-right-radius: 10px; border-bottom-right-radius: 10px; padding: 7px;")
        self.button = QPushButton()
        pixmap = QIcon(icon)
        self.button.setIcon(pixmap)
        self.button.setIconSize(QSize(33, 33))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; background-color : #fff;")
        self.the_line.addWidget(self.text_input)
        self.the_line.addWidget(self.button)
        self.button.clicked.connect(self.event_emittor)
        self.setLayout(self.the_line)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass
        else:
            super().mousePressEvent(event)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)

    def setText(self, txt):
        self.text_input.setText(txt)
        IconTextBoxAR.text_value = txt

    @staticmethod
    def text():
        return IconTextBoxAR.text_value

    def update_value(self, txt):
        IconTextBoxAR.text_value = txt

    def event_emittor(self):
        self.iconClicked.emit()
