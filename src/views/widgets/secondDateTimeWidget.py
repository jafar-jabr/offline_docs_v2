from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QSpacerItem, QSizePolicy, QComboBox
import datetime


class SecondDateTimeWidget(QWidget):
    def __init__(self, start_before, the_range):
        super().__init__()
        self.setFixedWidth(440)
        first_time_l = QHBoxLayout()
        #
        self.date = DateWidget(start_before, the_range)
        self.time = TimeWidget()
        #
        first_time_l.addWidget(self.date)
        first_time_l.addWidget(self.time)
        self.setLayout(first_time_l)

    def value(self):
        return self.date.value()+' '+self.time.value()


class TimeWidget(QWidget):
    hour_value = ""
    minute_value = ""
    am_pm_value = ""

    def __init__(self, **kwargs):
        super().__init__()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 20, 0) #(left, top, right, bottom)
        main_layout.setSpacing(0)
        h_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        h_select = QComboBox()
        for option in h_options:
            h_select.addItem(option)
        m_options = ["00", "05", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55"]
        m_select = QComboBox()
        for option in m_options:
            m_select.addItem(option)

        space_item = QSpacerItem(20, 20, QSizePolicy.Expanding)
        am_pm = QComboBox()
        am_pm.addItem("am")
        am_pm.addItem("pm")
        separator = QLabel(" : ")

        if "value" in kwargs:
            time_parts = kwargs["value"].split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            minute = self.myround(minute)
            the_hour, the_period = self.handle_am_pm(hour)

            TimeWidget.hour_value = str(the_hour)
            TimeWidget.minute_value = str(minute)
            TimeWidget.am_pm_value = the_period

            h_select.setCurrentText(str(the_hour))
            m_select.setCurrentText(str(minute))
            am_pm.setCurrentText(the_period)
        else:
            current_hour = datetime.datetime.now().hour
            current_minute = datetime.datetime.now().minute
            current_minute = self.myround(current_minute)
            the_hour, the_period = self.handle_am_pm(current_hour)
            h_select.setCurrentText(str(the_hour))
            m_select.setCurrentText(str(current_minute))
            am_pm.setCurrentText(the_period)

            TimeWidget.hour_value = str(the_hour)
            TimeWidget.minute_value = str(current_minute)
            TimeWidget.am_pm_value = the_period

        h_select.activated[str].connect(self.update_hour)
        m_select.activated[str].connect(self.update_minute)
        am_pm.activated[str].connect(self.update_am_pm)

        main_layout.addWidget(h_select)
        main_layout.addWidget(separator)
        main_layout.addWidget(m_select)
        main_layout.addSpacerItem(space_item)
        main_layout.addWidget(am_pm)

        self.setLayout(main_layout)
        # self.setFixedWidth(230)
        self.setFixedHeight(37)

    @staticmethod
    def value():
        the_hour = int(TimeWidget.hour_value)
        the_minute = TimeWidget.minute_value
        if TimeWidget.am_pm_value == "pm":
            the_hour = 12+int(TimeWidget.hour_value)
        if len(str(the_hour)) == 1:
            the_hour = "0"+str(the_hour)
        if len(TimeWidget.minute_value) == 1:
            the_minute = "0"+the_minute
        return str(the_hour)+":"+the_minute+":00"

    # def paintEvent(self, event):
    #     paint = QPainter(self)
    #     paint.setBrush(QColor("#f5f5f5"))
    #     pen = QPen()
    #     pen.setColor(QColor("#f5f5f5"))
    #     paint.setPen(pen)
    #     paint.drawRoundedRect(self.rect(), 10.0, 10.0)

    def handle_am_pm(self, hour):
        if hour > 12:
            return hour-12, "pm"
        else:
            return hour, "am"

    def update_hour(self, hour):
        TimeWidget.hour_value = hour

    def update_minute(self, minute):
        TimeWidget.minute_value = minute

    def update_am_pm(self, am_pm):
        TimeWidget.am_pm_value = am_pm

    @staticmethod
    def myround(x, base=5):
        return int(base * round(float(x) / base))


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

    # def paintEvent(self, event):
    #     paint = QPainter(self)
    #     paint.setBrush(QColor("#f5f5f5"))
    #     pen = QPen()
    #     pen.setColor(QColor("#f5f5f5"))
    #     paint.setPen(pen)
    #     paint.drawRoundedRect(self.rect(), 10.0, 10.0)

    def update_year(self, year):
        DateWidget.year_value = year

    def update_month(self, month):
        DateWidget.month_value = month

    def update_day(self, day):
        DateWidget.day_value = day
