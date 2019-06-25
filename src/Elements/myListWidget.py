import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class MyListWidget(QListWidget):
    listRightClicked = pyqtSignal(str)
    clicked = pyqtSignal(str)
    double_clicked = pyqtSignal(str)
    first_click_time = 0

    def __init__(self, h, w, **kwargs):
        super().__init__()
        self.installEventFilter(self)
        if "options" in kwargs:
            for opt in kwargs['options']:
                item = QListWidgetItem(opt)
                self.addItem(item)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.itemClicked.connect(self.list_item_clicked)
        self.setMinimumHeight(h)
        self.setFixedWidth(w)
        if 'bg_color'in kwargs:
            bg_color = kwargs['bg_color']
        else:
            bg_color = "#445566"

        if 'front_color'in kwargs:
            front_color = kwargs['front_color']
        else:
            front_color = "#ffffff"

        the_style = "QListWidget { background: %s;} " \
                    " QListWidget::item {" \
                    "border-style: solid;" \
                    " border-width:1px;" \
                    " border-color:black;" \
                    " color: %s;" \
                    " font-size: 16px;" \
                    "}" \
                    " QListWidget::item:selected { background-color: red;}" % (bg_color, front_color)
        self.setStyleSheet(the_style)

    def already_exist(self, old_prescription, selected_medicine):
        selected_medicine = selected_medicine.strip()
        prob_1 = selected_medicine
        prob_2 = ' '+selected_medicine
        prob_3 = selected_medicine+' '
        prob_4 = ' '+selected_medicine+' '
        prob_5 = selected_medicine+', '
        old_parts = old_prescription.split(',')
        for part in old_parts:
            if prob_1 in part or prob_2 in part or prob_3 in part or prob_4 in part or prob_5 in part:
                return True
        return False

    def list_item_clicked(self, item):
        self.clicked.emit(item.text())
        current = datetime.datetime.now()
        if not self.first_click_time:
            self.first_click_time = current
        else:
            diff = current - self.first_click_time
            if diff.microseconds < 255000:
                self.double_clicked.emit(item.text())
                self.first_click_time = current
                return
        self.first_click_time = current

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.ContextMenu and source is self:
            menu = QtWidgets.QMenu()
            menu.addAction('Delete')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.listRightClicked.emit(item.text())
            return True
        return super().eventFilter(source, event)

    def update_options(self, options, selected):
        for opt in options:
            self.remove_option(opt)
        for opt in options:
            self.addItem(opt)
            self.repaint()
        items = self.findItems(selected, Qt.MatchExactly)
        items[0].setSelected(True)
        self.scrollToItem(items[0], QtWidgets.QAbstractItemView.PositionAtTop)

    def only_update_options(self, options):
        self.clear()
        for opt in options:
            self.addItem(opt)
            self.repaint()

    def remove_option(self, t):
        items = self.findItems(t, Qt.MatchExactly)
        for item in items:
            self.takeItem(self.row(item))
            self.repaint()

    def add_line(self, valuee):
        self.addItem(valuee)
        self.repaint()
