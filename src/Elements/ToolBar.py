from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        parent.homeAction = QAction(QIcon("resources/assets/images/user_image.png"), 'Home Page')
        parent.homeAction.triggered.connect(lambda me: self.menu_action("home"))

        self.Buttons = [
            parent.homeAction,
        ]

    def menu_clicked(self):
        print("clicked")

    @pyqtSlot()
    def menu_action(self, which):
        # PlayMouth(self.parent).go_to(which)
        self.parent.close()
        from src.forms.landingForm import LandingForm
        window = LandingForm()
        window.show()
