from datetime import datetime
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import pyqtSlot, Qt
import pyscreenshot as ImageGrab
from src.views.modals.aboutModal import AboutModal


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        parent.homeAction = QAction(QIcon("resources/assets/images/homepage.png"), 'Home Page')
        parent.homeAction.triggered.connect(lambda me: self.menu_action("home"))

        parent.screenShootAction = QAction(QIcon("resources/assets/images/screen_shoot.png"), 'Take screen shoot')
        parent.screenShootAction.triggered.connect(self.take_screen_shoot)

        parent.aboutAction = QAction(QIcon("resources/assets/images/menu/about.png"), 'About The App')
        parent.aboutAction.triggered.connect(self.about_modal)

        self.Buttons = [
            parent.homeAction,
            parent.screenShootAction,
            parent.aboutAction,
        ]

    def menu_clicked(self):
        print("clicked")

    @pyqtSlot()
    def menu_action(self, which):
        # PlayMouth(self.parent).go_to(which)
        self.parent.close()
        from src.views.forms.landingForm import LandingForm
        window = LandingForm()
        window.show()

    def about_modal(self):
        AboutModal()

    def take_screen_shoot(self):
        self.parent.setWindowState(Qt.WindowMinimized)
        # grab fullscreen
        im = ImageGrab.grab()
        img_name = 'sc_sh_'+datetime.now().strftime("%m%d%Y%H%M%S")+'.png'
        options = QFileDialog.Options()
        the_path = str(QFileDialog.getExistingDirectory(self.parent, "choose where to save it!", '', options=options))
        if the_path:
            im.save(the_path+'/'+img_name)
        # save image file
        # show image in a window
        self.parent.setWindowState(Qt.WindowNoState)