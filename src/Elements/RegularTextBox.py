from PyQt5.QtWidgets import QLineEdit


class RegularTextBoxAR(QLineEdit):
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
