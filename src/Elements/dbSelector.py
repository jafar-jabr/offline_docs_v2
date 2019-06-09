from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QPushButton
from src.Elements.ClickableLineEdit import ClickableLineEdit


class DatabaseSelector(QWidget):
    db_url = ""

    def __init__(self, max_w=240):
        super().__init__()
        # DatabaseSelector.db_url = ""
        self.the_line = QHBoxLayout()
        self.the_line.setContentsMargins(0, 0, 0, 0)
        self.the_line.setSpacing(0)
        self.text = ClickableLineEdit()
        self.text.setFixedHeight(33)
        self.setMaximumWidth(max_w)
        self.text.setText("Choose Database")
        self.text.setReadOnly(True)
        self.text.clicked.connect(self.do_select_image)
        self.text.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; padding: 7px;")
        self.img_select_btn = QPushButton()
        self.img_select_btn.setAutoDefault(False)
        pixmap = QIcon("resources/assets/images/file.png")
        self.img_select_btn.setIcon(pixmap)
        self.img_select_btn.setIconSize(QSize(33, 33))
        self.img_select_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.img_select_btn.setStyleSheet("border-top-right-radius: 10px; border-bottom-right-radius: 10px; background-color : #fff;")
        self.the_line.addWidget(self.text)
        self.the_line.addWidget(self.img_select_btn)
        self.img_select_btn.clicked.connect(self.do_select_image)
        self.setLayout(self.the_line)

    def do_select_image(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        db_path, _ = QFileDialog.getOpenFileName(None, "Choose Database", "", "Database Files (*.db)", options=options)
        if db_path:
            DatabaseSelector.db_url = db_path
            self.text.setText(db_path)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)

    def setText(self, txt):
        self.text.setText(txt)

    @staticmethod
    def value():
        return DatabaseSelector.db_url
