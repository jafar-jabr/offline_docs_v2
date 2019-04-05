from PyQt5.QtCore import QDate, QLocale
from PyQt5.QtWidgets import QHBoxLayout, QDialog, QCalendarWidget


class CalendarModal:
    def __init__(self, parent, title="اختر التاريخ"):
        self.parent = parent
        win = QDialog()
        layout = QHBoxLayout()
        cal = QCalendarWidget()
        cal.setLocale(QLocale("AR"))
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.send_to_parent)
        layout.addWidget(cal)
        win.setLayout(layout)
        win.setWindowTitle(title)
        win.exec_()

        # cal.setMinimumDate(min)
        # cal.setMaximumDate(max)

    def send_to_parent(self, date):
        self.parent.setText(date.toString("yyyy-MM-dd"))
