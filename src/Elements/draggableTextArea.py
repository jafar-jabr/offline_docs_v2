from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTextEdit


class DraggableTextArea(QTextEdit):
    moved = pyqtSignal()
    lost_focus = pyqtSignal()

    def __init__(self, *args):
        super().__init__(*args)
        self.setFixedWidth(200)
        self.setFixedHeight(300)
        # self.setCursor(QCursor(Qt.PointingHandCursor))

    def focusOutEvent(self, event):
        if event.type() == QtCore.QEvent.FocusOut:
            self.lost_focus.emit()

    def mousePressEvent(self, event):
        self.bring_to_front()
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        super(DraggableTextArea, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            if self.__mouseMovePos is not None:
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                self.move(newPos)
                self.__mouseMovePos = globalPos
        super(DraggableTextArea, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos
            self.moved.emit()
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(DraggableTextArea, self).mouseReleaseEvent(event)

    def bring_to_front(self):
        self.show()
        self.activateWindow()
        self.raise_()
