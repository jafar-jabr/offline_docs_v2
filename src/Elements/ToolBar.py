from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QAction, QShortcut
from src.models.PlayMouth import PlayMouth
from PyQt5.QtCore import pyqtSlot


class ToolBar:
    def __init__(self, parent):
        self.parent = parent
        parent.homeAction = QAction(QIcon("resources/assets/images/menu/home.png"), 'الصفحة الرئيسية')
        # parent.homeAction.setCursor(QCursor(Qt.PointingHandCursor))
        parent.homeAction.triggered.connect(lambda me: self.menu_action("home"))

        parent.home_shortcut = QShortcut(QKeySequence("Ctrl+H"), parent)
        parent.home_shortcut.activated.connect(lambda: self.menu_action("home"))

        # parent.addStaff = QAction(QIcon("resources/assets/images/menu/add_doctor.png"), 'اضافة منتسب')
        # parent.addStaff.triggered.connect(lambda me: self.menu_action("add_staff"))

        parent.addPatient = QAction(QIcon("resources/assets/images/menu/add_patient.png"), 'اضافة مراجع')
        parent.addPatient.triggered.connect(lambda me: self.menu_action("add_patient"))

        parent.patient_shortcut = QShortcut(QKeySequence("Ctrl+N"), parent)
        parent.patient_shortcut.activated.connect(lambda: self.menu_action("add_patient"))

        # parent.staffAction = QAction(QIcon("resources/assets/images/menu/staff-settings.png"), 'المنتسبين')
        # parent.staffAction.triggered.connect(lambda me: self.menu_action("staff"))

        parent.clinicSettingsAction = QAction(QIcon("resources/assets/images/menu/staff-settings.png"), 'اعدادات المؤسسة والكادر')
        parent.clinicSettingsAction.triggered.connect(lambda me: self.menu_action("clinic_settings"))

        parent.clinic_shortcut = QShortcut(QKeySequence("Ctrl+S"), parent)
        parent.clinic_shortcut.activated.connect(lambda: self.menu_action("clinic_settings"))

        parent.accountSettingsAction = QAction(QIcon("resources/assets/images/menu/account-settings.png"), 'اعدادات الحساب')
        parent.accountSettingsAction.triggered.connect(lambda me: self.menu_action("account"))

        parent.clinic_shortcut = QShortcut(QKeySequence("Ctrl+M"), parent)
        parent.clinic_shortcut.activated.connect(lambda: self.menu_action("account"))

        parent.contactAction = QAction(QIcon("resources/assets/images/menu/contact.png"), 'الاتصال بنا')
        parent.contactAction.triggered.connect(lambda me: self.menu_action("contact"))

        parent.contact_shortcut = QShortcut(QKeySequence("Ctrl+T"), parent)
        parent.contact_shortcut.activated.connect(lambda: self.menu_action("contact"))

        parent.appSettingAction = QAction(QIcon("resources/assets/images/menu/app-settings.png"), 'اعدادات التطبيق')
        parent.appSettingAction.triggered.connect(lambda me: self.menu_action("app_settings"))

        parent.contact_shortcut = QShortcut(QKeySequence("Ctrl+G"), parent)
        parent.contact_shortcut.activated.connect(lambda: self.menu_action("app_settings"))

        parent.aboutAction = QAction(QIcon("resources/assets/images/menu/about.png"), 'حول')
        parent.aboutAction.triggered.connect(lambda me: self.menu_action("about"))

        parent.about_shortcut = QShortcut(QKeySequence("Ctrl+O"), parent)
        parent.about_shortcut.activated.connect(lambda: self.menu_action("about"))

        self.Buttons = [
            parent.homeAction,
            # parent.addStaff,
            parent.addPatient,
            # parent.staffAction,
            parent.clinicSettingsAction,
            parent.accountSettingsAction,
            parent.contactAction,
            parent.appSettingAction,
            parent.aboutAction
        ]

    @pyqtSlot()
    def menu_action(self, which):
        PlayMouth(self.parent).go_to(which)
