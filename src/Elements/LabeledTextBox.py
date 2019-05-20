from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel


class LabeledTextBoxAR(QLineEdit):
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


class LabeledTextBox(QWidget):
    text_value = ""

    def __init__(self, label, **kwargs):
        super().__init__()
        self.the_line = QHBoxLayout()
        if 'space' in kwargs:
            self.the_line.setSpacing(kwargs['space'])
        else:
            self.the_line.setSpacing(0)
        self.text_input = QLineEdit()
        self.text_input.setFixedHeight(33)
        self.text_input.textChanged[str].connect(self.update_value)
        if ('place_holder' in kwargs and 'text' not in kwargs) or ('place_holder' in kwargs and 'text' in kwargs and kwargs['text'].strip() == 0):
            self.text_input.setPlaceholderText(kwargs['place_holder'])
        elif 'text' in kwargs and kwargs['text'].strip() > 0:
            self.text_input.setText(kwargs['text'])
            LabeledTextBox.text_value = kwargs['text']
        # self.text_input.setStyleSheet("border-radius: 10px; padding: 7px;")
        self.text_input.setStyleSheet("border: 2px solid #BFBFC6;"
                                      "border-radius: 5px;"
                                      # "border-image: url(./resources/assets/images/Categories/textarea-bg.jpg)"
                                      )
        label = QLabel(label)
        self.the_line.addWidget(label)
        self.the_line.addWidget(self.text_input)
        self.setLayout(self.the_line)
        if 'width' in kwargs:
            self.setFixedWidth(kwargs['width'])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pass
        else:
            super().mousePressEvent(event)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)

    def setText(self, txt):
        self.text_input.setText(txt)
        LabeledTextBox.text_value = txt

    @staticmethod
    def text():
        return LabeledTextBox.text_value

    def update_value(self, txt):
        LabeledTextBox.text_value = txt
