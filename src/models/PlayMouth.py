from src.forms.AccountSettings import AccountSettings
from src.forms.AppSettings import AppSettings
from src.forms.GeneralSettings import GeneralSettings
from src.forms.addPatient import AddPatient
from src.forms.landingForm import LandingForm
from src.forms.loginForm import Login
from src.forms.patientDetails import PatientDetails
from src.forms.aboutForm import About
from src.forms.contactForm import ContactForm
from src.models.SharedFunctions import SharedFunctions


class PlayMouth:
    def __init__(self, app):
        self.app = app

    def go_to(self, which, **kwargs):
        new_widget = self.all_pages(which)(self.app, **kwargs)
        if which != 'contact' and which != 'about':
            check_point, do_order = SharedFunctions.check_point('internal')
            if not check_point:
                if do_order:
                    new_widget = About(self.app, order=True)
                    which = 'about'
                else:
                    new_widget = ContactForm(self.app, order=True)
                    which = 'contact'
        new_widget.update()
        self.app.central_widget.update()
        for i in range(self.app.central_widget.count()):
            widget = self.app.central_widget.widget(i)
            self.app.central_widget.removeWidget(widget)
            widget.deleteLater()
        self.app.central_widget.addWidget(new_widget)
        self.app.central_widget.setCurrentWidget(new_widget)
        self.app.setWindowTitle(self.page_titles(which))

    @staticmethod
    def all_pages(which):
        pages = {
            "home": LandingForm,
            "add_patient": AddPatient,
            "clinic_settings": GeneralSettings,
            "app_settings": AppSettings,
            "account": AccountSettings,
            "about": About,
            "contact": ContactForm,
            "patient_details": PatientDetails,
            "login": Login
        }
        return pages[which]

    @staticmethod
    def page_titles(which):
        titles = {
            "home": "Offline Docs / الصفحة الرئيسية",
            "add_staff": "Offline Docs / اضافة منتسب",
            "add_patient": "Offline Docs / اضافة مراجع",
            "staff": "Offline Docs / المنتسبون",
            "clinic_settings": "Offline Docs / اعدادات المؤسسة والكادر",
            "app_settings": "Offline Docs / اعدادات التطبيق",
            "account": "Offline Docs / اعدادات الحساب",
            "about": "Offline Docs / حول",
            "contact": "Offline Docs / الاتصال بنا",
            "patient_details": "Offline Docs / تفاصيل المراجع",
            "edit_patient": "Offline Docs / تعديل بيانات المراجع والزيارة",
            "login": "Offline Docs / تسجيل الدخول"
        }
        return titles[which]
