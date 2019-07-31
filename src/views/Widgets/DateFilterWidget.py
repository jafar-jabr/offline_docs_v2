from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QCursor, QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QComboBox, QCheckBox
import datetime


class DateFilterWidget(QWidget):
    year_value = ""
    month_value = ""
    day_value = ""
    clicked = pyqtSignal()

    def __init__(self, start_before, date_range, **kwargs):
        super().__init__()
        date_filter_font = QFont()
        date_filter_font.setPixelSize(16)
        self.setFont(date_filter_font)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(3, 0, 3, 0) #(left, top, right, bottom)
        main_layout.setSpacing(0)
        self.chk = FilterCheckBox()
        self.chk.stateChanged.connect(self.clickBox)
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day
        first_year = current_year - start_before + 1
        last_year = current_year - date_range
        year1 = min(last_year, first_year)
        year2 = max(last_year, first_year)
        years = range(year1, year2)
        self.y_select = QComboBox()
        self.y_select.setFont(date_filter_font)
        for option in reversed(years):
            self.y_select.addItem(str(option))
        self.m_select = QComboBox()
        self.m_select.setFont(date_filter_font)
        for month in range(12):
            self.m_select.addItem(str(month+1))
        self.d_select = QComboBox()
        self.d_select.setFont(date_filter_font)
        for option in range(31):
            self.d_select.addItem(str(option+1))

        separator = QLabel(" \ ")
        separator2 = QLabel(" \ ")
        separator3 = QLabel(" ")

        if "value" in kwargs:
            date_parts = kwargs["value"].split("-")
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])
            DateFilterWidget.year_value = str(year)
            DateFilterWidget.month_value = str(month)
            DateFilterWidget.day_value = str(day)
            self.y_select.setCurrentText(str(year))
            self.m_select.setCurrentText(str(month))
            self.d_select.setCurrentText(str(day))
        else:
            self.y_select.setCurrentText(str(current_year))
            self.m_select.setCurrentText(str(current_month))
            self.d_select.setCurrentText(str(current_day))
            DateFilterWidget.year_value = str(current_year)
            DateFilterWidget.month_value = str(current_month)
            DateFilterWidget.day_value = str(current_day)

        self.d_select.activated[str].connect(self.update_day)
        self.m_select.activated[str].connect(self.update_month)
        self.y_select.activated[str].connect(self.update_year)

        main_layout.addWidget(self.d_select)
        main_layout.addWidget(separator)
        main_layout.addWidget(self.m_select)
        main_layout.addWidget(separator2)
        main_layout.addWidget(self.y_select)
        main_layout.addWidget(separator3)
        main_layout.addWidget(self.chk)

        self.setLayout(main_layout)
        self.setFixedWidth(236)
        self.setFixedHeight(37)
        self.setLayoutDirection(Qt.RightToLeft)

    @staticmethod
    def value():
        if len(DateFilterWidget.month_value) == 1:
            DateFilterWidget.month_value = "0"+DateFilterWidget.month_value
        if len(DateFilterWidget.day_value) == 1:
            DateFilterWidget.day_value = "0"+DateFilterWidget.day_value
        return DateFilterWidget.year_value+"-"+DateFilterWidget.month_value+"-"+DateFilterWidget.day_value

    def setValue(self, date_str):
        date_parts = date_str.split("-")
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        DateFilterWidget.year_value = str(year)
        DateFilterWidget.month_value = str(month)
        DateFilterWidget.day_value = str(day)
        self.y_select.setCurrentText(str(year))
        self.m_select.setCurrentText(str(month))
        self.d_select.setCurrentText(str(day))

    # def paintEvent(self, event):
    #     paint = QPainter(self)
    #     paint.setBrush(QColor("#f5f5f5"))
    #     pen = QPen()
    #     pen.setColor(QColor("#f5f5f5"))
    #     paint.setPen(pen)
    #     paint.drawRoundedRect(self.rect(), 10.0, 10.0)

    def update_year(self, year):
        DateFilterWidget.year_value = year
        if self.chk.checkState() == Qt.Checked:
            self.clicked.emit()

    def update_month(self, month):
        DateFilterWidget.month_value = month
        if self.chk.checkState() == Qt.Checked:
            self.clicked.emit()

    def update_day(self, day):
        DateFilterWidget.day_value = day
        if self.chk.checkState() == Qt.Checked:
            self.clicked.emit()

    def clickBox(self, state):
        if state == Qt.Checked:
            self.clicked.emit()
        else:
            self.clicked.emit()
            self.reset()

    def reset(self):
        current_year = datetime.date.today().year
        current_month = datetime.date.today().month
        current_day = datetime.date.today().day
        self.y_select.setCurrentText(str(current_year))
        self.m_select.setCurrentText(str(current_month))
        self.d_select.setCurrentText(str(current_day))
        DateFilterWidget.year_value = str(current_year)
        DateFilterWidget.month_value = str(current_month)
        DateFilterWidget.day_value = str(current_day)
        self.chk.setChecked(False)

    def is_checked(self):
        if self.chk.checkState() == Qt.Checked:
            return True
        else:
            return False

    def setIsChecked(self):
        self.chk.setChecked(True)


class FilterCheckBox(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
               QCheckBox{
                   font-size: 18px;
               }
               QCheckBox::indicator {
                 width: 20px;
                 height: 20px;
               }
               QCheckBox::indicator:unchecked {
                   image: url(./resources/assets/images/checkbox/unchecked.png);
               }
               QCheckBox::indicator:unchecked:pressed {
                    image: url(./resources/assets/images/checkbox/unchecked-pressed);
                }

                QCheckBox::indicator:checked {
                    image: url(./resources/assets/images/checkbox/checked.png);
                }
                QCheckBox::indicator:checked:pressed {
                    image: url(./resources/assets/images/checkbox/checked-pressed.png);
                }
                QCheckBox::indicator:indeterminate:pressed {
                    image: url(./resources/assets/images/checkbox/checked.png);
                }
            """
        self.setStyleSheet(style)
