from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QSpacerItem, QSizePolicy, QComboBox
import datetime


class TimeWidget(QWidget):
    hour_value = ""
    minute_value = ""
    am_pm_value = ""

    def __init__(self, **kwargs):
        super().__init__()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(50, 0, 20, 0) #(left, top, right, bottom)
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
        am_pm.addItem("ص")
        am_pm.addItem("م")
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

        main_layout.addWidget(m_select)
        main_layout.addWidget(separator)
        main_layout.addWidget(h_select)
        main_layout.addSpacerItem(space_item)
        main_layout.addWidget(am_pm)

        self.setLayout(main_layout)
        self.setFixedWidth(230)
        self.setFixedHeight(37)
        self.setLayoutDirection(Qt.RightToLeft)

    @staticmethod
    def value():
        the_hour = int(TimeWidget.hour_value)
        the_minute = TimeWidget.minute_value
        if TimeWidget.am_pm_value == "م":
            the_hour = 12+int(TimeWidget.hour_value)
        if len(str(the_hour)) == 1:
            the_hour = "0"+str(the_hour)
        if len(TimeWidget.minute_value) == 1:
            the_minute = "0"+the_minute
        return str(the_hour)+":"+the_minute+":00"

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setBrush(QColor("#f5f5f5"))
        pen = QPen()
        pen.setColor(QColor("#f5f5f5"))
        paint.setPen(pen)
        paint.drawRoundedRect(self.rect(), 10.0, 10.0)

    def handle_am_pm(self, hour):
        if hour > 12:
            return hour-12, "م"
        else:
            return hour, "ص"

    def update_hour(self, hour):
        TimeWidget.hour_value = hour

    def update_minute(self, minute):
        TimeWidget.minute_value = minute

    def update_am_pm(self, am_pm):
        TimeWidget.am_pm_value = am_pm

    @staticmethod
    def myround(x, base=5):
        return int(base * round(float(x) / base))
