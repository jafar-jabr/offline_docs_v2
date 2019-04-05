from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QSize
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QWidget, QHBoxLayout, QSizePolicy, \
    QPushButton

from src.Elements.ClickableLineEdit import ClickableLineEdit
from src.Elements.CustomLabel import RegularLabel
from src.Elements.RegularTextArea import RegularTextArea


class PrescriptionInput(QWidget):
    iconClicked = pyqtSignal()
    listRightClicked = pyqtSignal(str)

    def __init__(self, h=110, w=700, label='', **kwargs):
        super().__init__()
        text_line = QHBoxLayout()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)) #width, height
        text_label = RegularLabel(label)
        text_width_reduction = 0
        if len(label) > 0:
            text_width_reduction = 240
        if "spacing" in kwargs:
            text_width_reduction = kwargs['spacing']
        if "text" in kwargs and kwargs['text'] is not None and len(kwargs['text'].strip()) > 0:
            self.text_body = RegularTextArea(h - 10, w - text_width_reduction, text=kwargs['text'])
        elif "placeHolder" in kwargs:
            self.text_body = RegularTextArea(h - 10, w - text_width_reduction, placeHolder=kwargs["placeHolder"])
        elif "placeHolder" not in kwargs and "text" not in kwargs:
            self.text_body = RegularTextArea(h - 10, w - text_width_reduction)

        text_line.addWidget(text_label)
        text_line.addWidget(self.text_body)

        other = QWidget()
        other.setContentsMargins(0, 0, 0, 0)
        other.setMaximumWidth(300)
        other.setFixedHeight(h)

        self.left_column = QVBoxLayout()
        self.left_column.setContentsMargins(0, 0, 0, 0)
        self.left_column.setSpacing(0)
        self.listWidget = QListWidget()
        self.listWidget.installEventFilter(self)
        for opt in kwargs['options']:
            item = QListWidgetItem(opt)
            self.listWidget.addItem(item)
        self.listWidget.itemClicked.connect(self.list_item_clicked)

        txt_widget = QWidget()
        txt_widget.setContentsMargins(0, 0, 0, 0)
        sub_txt_line = QHBoxLayout()
        sub_txt_line.setSpacing(0)

        self.txt = ClickableLineEdit()
        self.txt.setMaximumHeight(33)
        self.txt.setAlignment(Qt.AlignRight)
        self.txt.setStyleSheet("border-top-right-radius: 10px; border-bottom-right-radius: 10px; padding: 7px;")
        self.button = QPushButton()
        pixmap = QIcon("resources/assets/images/plus-blue.png")
        self.button.setIcon(pixmap)
        self.button.setIconSize(QSize(33, 33))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; background-color : #fff;")
        self.button.clicked.connect(self.icon_clicked)

        self.txt.textChanged[str].connect(self.text_changed)
        sub_txt_line.addWidget(self.txt)
        sub_txt_line.addWidget(self.button)

        txt_widget.setLayout(sub_txt_line)

        self.left_column.addWidget(txt_widget)
        self.listWidget.setCursor(QCursor(Qt.PointingHandCursor))
        self.left_column.addWidget(self.listWidget)
        other.setLayout(self.left_column)

        text_line.addWidget(other)

        self.setLayout(text_line)
        self.setFixedWidth(w)
        text_line.setAlignment(Qt.AlignTop)
        self.setMinimumHeight(h)

    def toPlainText(self):
        return self.text_body.toPlainText()

    def clear(self):
        self.text_body.setText('')

    def setPlainText(self, txt):
        self.text_body.setText(txt)

    def text_changed(self, t):
        items = self.listWidget.findItems(t, Qt.MatchContains)
        if len(items):
            items[0].setSelected(True)
            self.listWidget.scrollToItem(items[0], QtWidgets.QAbstractItemView.PositionAtTop)

    def list_item_clicked(self):
        items = self.listWidget.selectedItems()
        old_prescription = self.toPlainText()
        if len(old_prescription):
            new_prescription = old_prescription+', ' + items[0].text()
        else:
            new_prescription = items[0].text()
        self.setPlainText(new_prescription)

    def icon_clicked(self):
        self.iconClicked.emit()

    def get_sub_text(self):
        return self.txt.text()

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self.listWidget:
            menu = QtWidgets.QMenu()
            menu.addAction('حذف')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.listRightClicked.emit(item.text())
            return True
        return super().eventFilter(source, event)

    def update_options(self, options, selected):
        for opt in options:
            self.listWidget.addItem(opt)
            self.listWidget.repaint()
        items = self.listWidget.findItems(selected, Qt.MatchExactly)
        items[0].setSelected(True)
        self.listWidget.scrollToItem(items[0], QtWidgets.QAbstractItemView.PositionAtTop)

    def remove_option(self, t):
        items = self.listWidget.findItems(t, Qt.MatchExactly)
        for item in items:
            self.listWidget.takeItem(self.listWidget.row(item))
