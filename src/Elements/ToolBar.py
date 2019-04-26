from PyQt5.QtGui import QIcon, QKeySequence, QCursor
from PyQt5.QtWidgets import QAction, QShortcut, QMenu


from src.models.PlayMouth import PlayMouth
from PyQt5.QtCore import pyqtSlot, QPoint, QEvent


class MyQAction(QAction):
    def __init__(self, *args):
        super().__init__(*args)
        self.images_menu = QMenu()
        opt = ['معاينة', 'تحديث', 'حذف']
        for i in opt:
            actn = QAction(QIcon('resources/assets/images/drop_down_h.png'), i, self.images_menu)
            actn.setObjectName(i)
            actn.triggered.connect(self.menu_clicked)
            self.images_menu.addAction(actn)

    def mousePressEvent(self, event):
        self.img_clicked(event.pos())
        print("clicked")

    def img_clicked(self, pos):
        parentPosition = self.mapToGlobal(QPoint(0, 0))
        menuPosition = parentPosition + pos
        self.images_menu.move(menuPosition)
        self.images_menu.show()

    def menu_clicked(self):
        which = self.sender().objectName()
        if which == "معاينة":
            print("review")
        elif which == "تحديث":
            print("update")
        elif which == "حذف":
            print("delete")


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        parent.homeAction = MyQAction(QIcon("resources/assets/images/user_image.png"), 'My Account')
        # parent.homeAction.installEventFilter(self.parent)
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
