from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from src.views.widgets.CustomLabel import RegularLabel


class AboutModal(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("create_account_modal")
        self.line_width = 480
        self.layout = QVBoxLayout()
        self.result = "try"
        self.registered_email = ""
        self.registered_password = ""
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 150)  # (left, top, right, bottom)
        nameLabel = RegularLabel('Offline Doc. v2')
        dateLabel = RegularLabel('Release Date: 2019-07-01')
        codeLabel = RegularLabel('Coded By: Jafar Jabr @ https://github.com/jafaronly')
        designLabel = RegularLabel('Graphic Design: Alex Simache @ https://github.com/alexsimache')
        self.layout.addWidget(nameLabel)
        self.layout.addWidget(dateLabel)
        self.layout.addWidget(codeLabel)
        self.layout.addWidget(designLabel)
        self.setWindowTitle("About App")

        self.resize(600, 370)
        self.setLayout(self.layout)
        self.exec_()
