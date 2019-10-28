from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import qrcode
import os

from src.views.widgets.LabeledTextBox import LabeledTextBox


class QrCodeGenerator(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("my_calendar_page")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QR Code Generator")
        self.show_file_browser = True
        self.img_url = ""
        layout = QVBoxLayout(self)
        # label0 = QLabel("Simple QR Code generator: ")
        self.qr_text = LabeledTextBox("Text to be converted to QR Code:       ", width=self.width()+400)
        self.qr_text.setText("")
        layout.addWidget(self.qr_text)

        self.figure = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        btn2 = QPushButton('Generate Code')
        btn2.clicked.connect(lambda me: self.generate_qr())
        layout.addWidget(btn2)

        self.resize(500, 500)
        self.show_image()

    def generate_qr(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        txt = self.qr_text.text()
        if len(txt):
            if len(txt.strip()):
                qr.add_data(txt)
                qr.make(fit=True)
                img = qr.make_image()
                qr_directory = './resources/data/qrCodes'
                qr_file = qr_directory+"/qr_code.jpg"
                if not os.path.exists(qr_directory):
                    os.makedirs(qr_directory)
                img.save(qr_file)
                self.show_image(img_path=qr_file)
                return
        self.show_image()

    def show_image(self, img_path="resources/assets/images/no_image.png"):
        plt.close('all')
        plt.gca().axes.get_yaxis().set_visible(False)
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        ax.set_axis_off()
        ax.set_title('Empty Image')
        # discards the old graph
        ax.clear()
        ax.grid(False)
        ax.tick_params(
            axis='both',
            which='both',
            bottom=False,
            top=False,
            right=False,
            left=False,
            labelbottom=False,
            labelleft=False)

        dd = plt.imread(img_path)
        # plot data
        ax.imshow(dd)
        # refresh canvas
        self.canvas.draw()
