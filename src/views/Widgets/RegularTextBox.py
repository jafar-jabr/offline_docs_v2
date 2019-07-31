from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class RegularTextBox(QLineEdit):
    def __init__(self, width=250, **kwargs):
        super().__init__()
        self.setMaximumWidth(width)
        self.setFixedHeight(33)
        self.setStyleSheet("border-radius: 10px; padding: 7px;")
        if "text" in kwargs:
            if type(kwargs['text']) == int:
                txt = str(kwargs['text'])
            else:
                txt = kwargs['text']
            self.setText(txt)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)


class CodeTextBoxAR(QLineEdit):
    inserted = pyqtSignal()

    def __init__(self, width=250, **kwargs):
        super().__init__()
        self.setMaximumWidth(width)
        self.setFixedHeight(33)
        self.setStyleSheet("border-radius: 10px; padding: 7px;")
        if "text" in kwargs:
            if type(kwargs['text']) == int:
                txt = str(kwargs['text'])
            else:
                txt = kwargs['text']
            self.setText(txt)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)

    def keyPressEvent(self, event):
        if event.key() != Qt.Key_Backspace and event.key() != Qt.Key_Delete:
            self.inserted.emit()
        super().keyPressEvent(event)
