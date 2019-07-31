from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


class PwdTextBoxAR(QLineEdit):
    def __init__(self, width=250, **kwargs):
        super().__init__()
        self.setMaximumWidth(width)
        self.setFixedHeight(37)
        self.setAlignment(Qt.AlignRight)
        self.setEchoMode(QLineEdit.Password)
        self.setStyleSheet(" border-radius: 10px; padding: 7px;")
        if "text" in kwargs:
            self.setText(kwargs['text'])

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)
