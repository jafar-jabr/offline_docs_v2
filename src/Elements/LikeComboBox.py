from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget


class LikeComboBox(QWidget):
    def __init__(self, txt="Test", **kwargs):
        super().__init__()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(50, 0, 20, 0) #(left, top, right, bottom)
        main_layout.setSpacing(0)
        self.widget_label = QLabel(txt)
        main_layout.addWidget(self.widget_label)
        self.setLayout(main_layout)
        self.setFixedWidth(230)
        self.setFixedHeight(37)
        self.setLayoutDirection(Qt.RightToLeft)

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setBrush(QColor("#f5f5f5"))
        pen = QPen()
        pen.setColor(QColor("#f5f5f5"))
        paint.setPen(pen)
        paint.drawRoundedRect(self.rect(), 10.0, 10.0)

    def currentText(self):
        return self.widget_label.text()
