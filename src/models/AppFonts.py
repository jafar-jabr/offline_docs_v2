from PyQt5.QtGui import QFont


class RegularFont(QFont):
    def __init__(self, size=16):
        super().__init__()
        self.setPixelSize(size)


