from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QImage, QPainter, QPixmap, QWindow
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


def maskImage(imgpath, imgtype='jpg', size=180):
    """Return a ``QPixmap`` from *imgdata* masked with a smooth circle.

    *imgdata* are the raw image bytes, *imgtype* denotes the image type.

    The returned image will have a size of *size* × *size* pixels.

    """

    imgdata = open(imgpath, 'rb').read()

    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)

    # Create the output image with the same dimensions and an alpha channel
    # and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle with the original image onto
    # the output image:
    brush = QBrush(image)        # Create texture brush
    painter = QPainter(out_img)  # Paint the output image
    painter.setBrush(brush)      # Use the image texture brush
    painter.setPen(Qt.NoPen)     # Don't draw an outline
    painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
    painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
    painter.end()                # We are done (segfault if you forget this)
    # Convert the image to a pixmap and rescale it.  Take pixel ratio into
    # account to get a sharp image on retina displays:
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return pm


class Window(QWidget):
    """Simple window that shows our masked image and text label."""
    def __init__(self):
        super().__init__()
        imgpath = "/home/jafar/PycharmProjects/PyQt5/images/logo.png"
        pixmap = maskImage(imgpath, "png")
        ilabel = QLabel()
        ilabel.setPixmap(pixmap)
        tlabel = QLabel('Hello, world!')

        layout = QVBoxLayout()
        layout.addWidget(ilabel, 0, Qt.AlignCenter)
        layout.addWidget(tlabel, 0, Qt.AlignCenter)
        self.setLayout(layout)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())