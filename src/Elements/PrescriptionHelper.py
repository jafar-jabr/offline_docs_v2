from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRect, Qt, pyqtSignal, QSize
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QWidget, QHBoxLayout, QSizePolicy, \
    QPushButton
from src.Elements.ClickableLineEdit import ClickableLineEdit


class PrescriptionHelper(QWidget):
    iconClicked = pyqtSignal()
    listRightClicked = pyqtSignal(str)

    def __init__(self, h, target, **kwargs):
        super().__init__()
        self.target = target
        text_line = QHBoxLayout()
        other = QWidget()
        other.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        other.setMaximumWidth(200)
        other.setFixedHeight(h)

        self.left_column = QVBoxLayout()
        self.left_column.setAlignment(Qt.AlignTop)
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
        self.txt.setStyleSheet("border-top-right-radius: 10px; border-bottom-right-radius: 10px;")
        self.button = QPushButton()
        self.button.setContentsMargins(0, 0, 0, 0)
        pixmap = QIcon("resources/assets/images/plus-blue.png")
        self.button.setIcon(pixmap)
        self.button.setIconSize(QSize(33, 33))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; background-color : #fff;")
        self.button.clicked.connect(self.icon_clicked)

        self.txt.textChanged[str].connect(self.text_changed)
        sub_txt_line.setContentsMargins(0, 0, 0, 0)
        sub_txt_line.addWidget(self.txt)
        sub_txt_line.addWidget(self.button)

        txt_widget.setLayout(sub_txt_line)

        self.left_column.addWidget(txt_widget)
        self.listWidget.setCursor(QCursor(Qt.PointingHandCursor))
        self.left_column.addWidget(self.listWidget)
        other.setLayout(self.left_column)
        other.setContentsMargins(0, 0, 0, 0)
        text_line.addWidget(other)

        self.setLayout(text_line)
        text_line.setAlignment(Qt.AlignTop)
        self.setMinimumHeight(h)

    def text_changed(self, t):
        items = self.listWidget.findItems(t, Qt.MatchContains)
        if len(items):
            items[0].setSelected(True)
            self.listWidget.scrollToItem(items[0], QtWidgets.QAbstractItemView.PositionAtTop)

    def list_item_clicked(self):
        items = self.listWidget.selectedItems()
        selected_medicine = items[0].text()
        old_prescription = self.target.toPlainText().strip()
        if len(old_prescription):
            if not self.already_exist(old_prescription, selected_medicine):
                new_prescription = old_prescription+', ' + selected_medicine
            else:
                new_prescription = old_prescription
        else:
            new_prescription = selected_medicine
        self.target.setPlainText(new_prescription)

    def already_exist(self, old_prescription, selected_medicine):
        prob_1 = selected_medicine
        prob_2 = ' '+selected_medicine
        prob_3 = selected_medicine+' '
        prob_4 = ' '+selected_medicine+' '
        old_parts = old_prescription.split(',')
        for part in old_parts:
            if prob_1 in part or prob_2 in part or prob_3 in part or prob_4 in part:
                return True
        return False

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
