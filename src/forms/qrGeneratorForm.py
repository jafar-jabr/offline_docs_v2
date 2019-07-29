from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import qrcode

from src.Elements.LabeledTextBox import LabeledTextBox


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
                img = qr.make_image(fill_color="black", back_color="white")
                self.show_qr(img)
                return
        self.show_image()

    def show_qr(self, img):
        plt.close('all')
        plt.gca().axes.get_yaxis().set_visible(False)
        # plt.xticks([])
        # plt.yticks([])
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title('Original Image')
        ax.clear()
        ax.grid(False)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.imshow(img)
        self.canvas.draw()

    def show_image(self, img_path="resources/assets/images/no_image.png"):
        plt.close('all')
        plt.gca().axes.get_yaxis().set_visible(False)
        self.figure.clear()
        # create an axis
        ax = self.figure.add_subplot(111)
        ax.set_title('Original Image')
        # discards the old graph
        ax.clear()
        ax.grid(False)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        dd = plt.imread(img_path)
        # plot data
        ax.imshow(dd)
        # refresh canvas
        self.canvas.draw()
