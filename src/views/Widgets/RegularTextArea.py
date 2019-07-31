from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit


class RegularTextArea(QTextEdit):
    def __init__(self, h=110, w=700, **kwargs):
        super().__init__()
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        self.setStyleSheet("border-radius:10px; background-color: palette(base);")
        self.setAlignment(Qt.AlignRight)
        if "text" in kwargs and kwargs['text'] is not None and len(kwargs['text'].strip()) > 0:
            self.setText(kwargs['text'])
        elif "placeHolder" in kwargs:
            self.setPlaceholderText(kwargs["placeHolder"])

    def clear(self):
        self.setText('')
