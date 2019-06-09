from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot

from src.modals.aboutModal import AboutModal


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        parent.homeAction = QAction(QIcon("resources/assets/images/homepage.png"), 'Home Page')
        parent.homeAction.triggered.connect(lambda me: self.menu_action("home"))

        parent.aboutAction = QAction(QIcon("resources/assets/images/menu/about.png"), 'About The App')
        parent.aboutAction.triggered.connect(self.about_modal)

        self.Buttons = [
            parent.homeAction,
            parent.aboutAction,
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

    def about_modal(self):
        AboutModal()
