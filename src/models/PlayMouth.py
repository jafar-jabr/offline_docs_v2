from src.forms.categoryForm import CategoryForm
from src.forms.dateTimeDifferenceForm import DateTimeDifferenceForm
from src.forms.documentsForm import DocumentsForm
from src.forms.qrGeneratorForm import QrCodeGenerator
from src.forms.randomGeneratorForm import RandomGeneratorForm


class PlayMouth:
    def __init__(self, app):
        self.app = app

    def go_to(self, which, **kwargs):
        new_widget = self.all_pages(which)(self.app, **kwargs)
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
            "categories": CategoryForm,
            "documents": DocumentsForm,
            'date_time_difference': DateTimeDifferenceForm,
            'random_generator': RandomGeneratorForm,
            'qr_generator': QrCodeGenerator,
        }
        return pages[which]

    @staticmethod
    def page_titles(which):
        titles = {
            "categories": "Offline Documentation/ Categories",
            "documents": "Offline Documentation/ Documents",
            "utilities": "Offline Documentation/ Utilities",
            "random_generator": "Offline Documentation/ Random Generator",
            "date_time_difference": "Offline Documentation/ DateTime difference",
            'qr_generator': "Offline Documentation/ QR Code generator",
        }
        return titles[which]
