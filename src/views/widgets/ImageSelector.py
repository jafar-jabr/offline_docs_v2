from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QPushButton
from src.views.widgets.ClickableLineEdit import ClickableLineEdit


class ImageSelector(QWidget):
    image_url = ""

    def __init__(self, max_w=240):
        super().__init__()
        # ImageSelector.image_url = ""
        self.the_line = QHBoxLayout()
        self.the_line.setContentsMargins(0, 0, 0, 0)
        self.the_line.setSpacing(0)
        self.text = ClickableLineEdit()
        self.text.setFixedHeight(33)
        self.setMaximumWidth(max_w)
        self.text.setText("Choose Database")
        self.text.setReadOnly(True)
        self.text.clicked.connect(self.do_select_image)
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
        self.button.clicked.connect(self.do_select_image)
        self.setLayout(self.the_line)

    def do_select_image(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        img_path, _ = QFileDialog.getOpenFileName(None, "اختر الصورة", "",
                                                  "Image Files (*.jpg *.png)", options=options)
        if img_path:
            ImageSelector.image_url = img_path
            self.text.setText(img_path)

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
        return ImageSelector.image_url
