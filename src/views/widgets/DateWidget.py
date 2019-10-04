from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QComboBox
import datetime


class DateWidget(QWidget):
    year_value = ""
    month_value = ""
    day_value = ""

    def __init__(self, start_before, date_range, **kwargs):
        super().__init__()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 10, 0) #(left, top, right, bottom)
        main_layout.setSpacing(0)
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day
        first_year = current_year - start_before + 1
        last_year = current_year - date_range
        year1 = min(last_year, first_year)
        year2 = max(last_year, first_year)
        years = range(year1, year2)
        y_select = QComboBox()
        for option in reversed(years):
            y_select.addItem(str(option))
        m_select = QComboBox()
        for month in range(12):
            m_select.addItem(str(month+1))
        d_select = QComboBox()
        for option in range(31):
            d_select.addItem(str(option+1))

        separator = QLabel(" \ ")
        separator2 = QLabel(" \ ")

        if "value" in kwargs:
            date_parts = kwargs["value"].split("-")
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            DateWidget.year_value = str(year)
            DateWidget.month_value = str(month)
            DateWidget.day_value = str(day)
            y_select.setCurrentText(str(year))
            m_select.setCurrentText(str(month))
            d_select.setCurrentText(str(day))
        else:
            y_select.setCurrentText(str(current_year))
            m_select.setCurrentText(str(current_month))
            d_select.setCurrentText(str(current_day))
            DateWidget.year_value = str(current_year)
            DateWidget.month_value = str(current_month)
            DateWidget.day_value = str(current_day)

        d_select.activated[str].connect(self.update_day)
        m_select.activated[str].connect(self.update_month)
        y_select.activated[str].connect(self.update_year)

        main_layout.addWidget(d_select)
        main_layout.addWidget(separator)
        main_layout.addWidget(m_select)
        main_layout.addWidget(separator2)
        main_layout.addWidget(y_select)

        self.setLayout(main_layout)
        self.setFixedWidth(230)
        self.setFixedHeight(37)
        self.setLayoutDirection(Qt.RightToLeft)

    @staticmethod
    def value():
        if len(DateWidget.month_value) == 1:
            DateWidget.month_value = "0"+DateWidget.month_value
        if len(DateWidget.day_value) == 1:
            DateWidget.day_value = "0"+DateWidget.day_value
        return DateWidget.year_value+"-"+DateWidget.month_value+"-"+DateWidget.day_value

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setBrush(QColor("#f5f5f5"))
        pen = QPen()
        pen.setColor(QColor("#f5f5f5"))
        paint.setPen(pen)
        paint.drawRoundedRect(self.rect(), 10.0, 10.0)

    def update_year(self, year):
        DateWidget.year_value = year

    def update_month(self, month):
        DateWidget.month_value = month

    def update_day(self, day):
        DateWidget.day_value = day
