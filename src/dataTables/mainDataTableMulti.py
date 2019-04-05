import math

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QSizePolicy, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, \
    QAbstractItemView, QLabel
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.CustomLabel import CustomLabel, RegularLabel
from src.Elements.DateFilterWidget import DateFilterWidget
from src.Elements.FilterTextBoxAR import FilterTextBoxAR
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.filteredCompoBox import FilteredCombo
from src.Elements.regularCompoBox import RegularCompoBox
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class MainDataTableMulti(QWidget):
    def __init__(self, grand_father, *args):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.table_w = SessionWrapper.get_dimension('main_table_w')
        self.current_label = QLabel()
        self.current_page = 1
        self.per_page = 10
        self.total_patients = 0
        self.grand_father = grand_father
        self.clinic_id = SessionWrapper.clinic_id
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.table.setFixedHeight(int(self.pc_height*0.35))
        self.table.setFixedWidth(self.table_w)

        header_stylesheet = "::section{Background-color:#99d8ff; height: 40px; font-size: 18px; }"
        self.table.horizontalHeader().setStyleSheet(header_stylesheet)
        number_stylesheet = "::section{Background-color:#99d8ff; }"
        self.table.verticalHeader().setStyleSheet(number_stylesheet)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        main_layout.setSpacing(10)

        filters = QHBoxLayout()
        filters.setAlignment(Qt.AlignLeft)
        filters.setSpacing(0)
        self.search_input = FilterTextBoxAR(260, False, "resources/assets/images/search.png", "البحث")
        self.the_note = RegularLabel("المجموع " + str(self.total_patients))
        filters.setContentsMargins(0, 30, 0, 0)  # (left, top, right, bottom)
        doctor_filter = RegularLabel('الترشيح بواسطة ::      الطبيب : ')
        doctor_options = Database().select_all_doctors(self.clinic_id)
        formatted_doctors_options = SharedFunctions.format_doctors_list(doctor_options, "كل الاطباء")
        self.doctor_filter_select = FilteredCombo(formatted_doctors_options)
        self.doctor_filter_select.activated[str].connect(self.do_filter)
        if SessionWrapper.search_wrapper['doctor']:
            self.doctor_filter_select.setCurrentText(SessionWrapper.search_wrapper['doctor'])

        status_filter = RegularLabel('    حالة المراجعة : ')
        status_options = ["الكل", "المجدولة", "الكاملة", "الملغية"]
        self.status_filter_select = RegularCompoBox(status_options)
        self.status_filter_select.activated[str].connect(self.do_filter)

        if SessionWrapper.search_wrapper['status']:
            self.status_filter_select.setCurrentText(SessionWrapper.search_wrapper['status'])

        date_line = QHBoxLayout()
        date_line.setSpacing(0)

        date_filter = RegularLabel('    التاريخ : ')
        self.date_filter_select = DateFilterWidget(-5, 5)
        self.date_filter_select.clicked.connect(self.do_filter)

        if SessionWrapper.search_wrapper['date']:
            self.date_filter_select.setValue(SessionWrapper.search_wrapper['date'])
            self.date_filter_select.setIsChecked()
        date_line.addWidget(date_filter)
        date_line.addWidget(self.date_filter_select)

        filters.addWidget(doctor_filter)
        filters.addWidget(self.doctor_filter_select)
        filters.addWidget(status_filter)
        filters.addWidget(self.status_filter_select)
        filters.addLayout(date_line)

        noteLine = QHBoxLayout()
        noteLine.setContentsMargins(15, 10, 0, 20)  # (left, top, right, bottom)

        if SessionWrapper.search_wrapper['free_search']:
            self.search_input.setText(SessionWrapper.search_wrapper['free_search'])
        self.search_input.iconClicked.connect(self.do_filter)
        noteLine.addWidget(self.the_note)
        noteLine.addWidget(self.search_input)
        main_layout.addLayout(filters)
        main_layout.addLayout(noteLine)
        main_layout.addWidget(self.table)
        # pagination = self.create_pagination()
        main_layout.addLayout(self.create_pagination())
        self.setLayout(main_layout)
        data, self.total_pages, self.total_patients = self.get_data(**self.get_active_filter())
        self.current_label.setText(str(self.current_page) + " من " + str(self.total_pages))
        self.the_note = RegularLabel("المجموع " + str(self.total_patients))
        self.setmydata(data)

    def updateFromDict(self, data):
        self.table.clear()
        self.table.clearContents()
        self.setmydata(data)
        self.current_label.setText(str(self.current_page) + " من " + str(self.total_pages))
        self.the_note.setText("المجموع " + str(self.total_patients))

    def setmydata(self, data):
        table_width = self.table_w
        headers = ["اسم المراجع", "تاريخ الميلاد", "رقم الهاتف", "عدد الزيارات", "تاريخ المراجعة", "الوقت", "الطبيب",
                   "حالة المراجعة", "اخرى"]
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setColumnWidth(0, math.floor(table_width*0.19))
        self.table.setColumnWidth(1, math.floor(table_width*0.109))
        self.table.setColumnWidth(2, math.floor(table_width*0.109))
        self.table.setColumnWidth(3, math.floor(table_width*0.101))
        self.table.setColumnWidth(4, math.floor(table_width*0.1))
        self.table.setColumnWidth(5, math.floor(table_width*0.1))
        self.table.setColumnWidth(6, math.floor(table_width*0.14))
        self.table.setColumnWidth(7, math.floor(table_width*0.081))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels([" "+str(i+1+((self.current_page-1)*self.per_page))+" " for i, row in enumerate(data)])
        for row_index, row in enumerate(data):
            for column_index, cell in enumerate(row):
                cell = str(cell)
                if column_index == len(headers)-1:
                    btn1 = ClickableIcon(25, 25, 'resources/assets/images/seemore-icon-circle.png')
                    btn1.setObjectName(cell)
                    btn1.clicked.connect(self.details_clicked)
                    btn2 = ClickableIcon(25, 25, 'resources/assets/images/delete-icon-blue10.png')
                    btn2.setObjectName(cell)
                    btn2.clicked.connect(self.delete_patient)
                    btn_layout = QHBoxLayout()
                    btn_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
                    btn_layout.addWidget(btn1)
                    btn_layout.addWidget(btn2)
                    container = QWidget()
                    container.setLayout(btn_layout)
                    self.table.setCellWidget(row_index, column_index, container)
                elif column_index == len(headers)-4:
                    the_time = SharedFunctions.readableTime(cell)
                    self.table.setItem(row_index, column_index, QTableWidgetItem(the_time))
                else:
                    c_cell = SharedFunctions.maybeLongString(cell)
                    self.table.setItem(row_index, column_index, QTableWidgetItem(c_cell))

    def details_clicked(self):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.grand_father).go_to("patient_details", visit_id=self.sender().objectName())

    def create_pagination(self):
        pagination_row = QHBoxLayout()

        btn_last = ClickableIcon(25, 25, "resources/assets/images/pagination/last.png")
        btn_last.clicked.connect(lambda: self.do_pagination("first"))
        pagination_row.addWidget(btn_last)

        btn_f = ClickableIcon(25, 25, "resources/assets/images/pagination/next.png")
        btn_f.clicked.connect(lambda: self.do_pagination("down"))
        pagination_row.addWidget(btn_f)

        pagination_row.addWidget(self.current_label)
        btn_b = ClickableIcon(25, 25, "resources/assets/images/pagination/prev.png")
        btn_b.clicked.connect(lambda: self.do_pagination("up"))
        pagination_row.addWidget(btn_b)

        btn_first = ClickableIcon(25, 25, "resources/assets/images/pagination/first.png")
        btn_first.clicked.connect(lambda: self.do_pagination("last"))
        pagination_row.addWidget(btn_first)

        pagination_row.setAlignment(Qt.AlignHCenter)
        return pagination_row

    def get_data(self, **kwargs):
        return Database().select_for_grid(self.clinic_id, self.current_page, self.per_page, **kwargs)

    def do_pagination(self, direction):
        if direction == "last":
            self.current_page = self.total_pages
        elif direction == "first":
            self.current_page = 1
        elif direction == "down":
            self.current_page = self.current_page - 1
            if self.current_page <= 0:
                self.current_page = 1
        elif direction == "up":
            self.current_page = self.current_page + 1
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
        data, self.total_pages, self.total_patients = self.get_data(**self.get_active_filter())
        self.updateFromDict(data)

    def do_filter(self, any=""):
        self.current_page = 1
        data, self.total_pages, self.total_patients = self.get_data(**self.get_active_filter())
        self.updateFromDict(data)

    def reset_filters(self, the_exception=None):
        filters = [self.doctor_filter_select, self.status_filter_select, self.date_filter_select, self.search_input]
        SessionWrapper.search_wrapper['doctor'] = 0
        SessionWrapper.search_wrapper['status'] = 0
        SessionWrapper.search_wrapper['date'] = 0
        SessionWrapper.search_wrapper['free_search'] = 0
        for the_filter in filters:
            if the_filter != the_exception:
                if the_filter == self.doctor_filter_select:
                    self.doctor_filter_select.setCurrentText("كل الاطباء")
                if the_filter == self.status_filter_select:
                    self.status_filter_select.setCurrentText("الكل")
                if the_filter == self.date_filter_select:
                    self.date_filter_select.reset()
                if the_filter == self.search_input:
                    self.search_input.setText("")

    def get_active_filter(self):
        filters = [self.doctor_filter_select, self.status_filter_select, self.date_filter_select, self.search_input]
        active_filter = {}
        for the_filter in filters:
            if the_filter == self.doctor_filter_select:
                if the_filter.currentText() != "كل الاطباء":
                    active_filter["doctor_filter"] = the_filter.currentText()
                    SessionWrapper.search_wrapper['doctor'] = the_filter.currentText()
                else:
                    SessionWrapper.search_wrapper['doctor'] = 0
            if the_filter == self.status_filter_select:
                if the_filter.currentText() != "الكل":
                    active_filter["status_filter"] = the_filter.currentText()
                    SessionWrapper.search_wrapper['status'] = the_filter.currentText()
                else:
                    SessionWrapper.search_wrapper['status'] = 0
            if the_filter == self.date_filter_select:
                if the_filter.is_checked():
                    active_filter["date_filter"] = the_filter.value()
                    SessionWrapper.search_wrapper['date'] = the_filter.value()
                else:
                    SessionWrapper.search_wrapper['date'] = 0
            if the_filter == self.search_input:
                plain_search = the_filter.text().strip()
                if plain_search != "":
                    active_filter["plain_search"] = the_filter.text()
                    SessionWrapper.search_wrapper['free_search'] = the_filter.text()
                else:
                    SessionWrapper.search_wrapper['free_search'] = 0
        return active_filter

    def delete_patient(self):
        if not SharedFunctions.is_manager():
            MessageBoxes.warning_message("خطأ", "ليس لديك الصلاحية للقيام بذلك")
            return
        visit_id = self.sender().objectName()
        details = Database().get_patient_and_visit(visit_id)
        patient_id = details["id"]
        patient_name = details["patient_name"]
        txt = "هل انت متأكد من رغبتك بحذف كل بيانات "+patient_name +"؟"
        confirm = MessageBoxes.confirm_message(txt)
        if confirm:
            Database().delete_patient(patient_id)
            data, self.total_pages, self.total_patients = self.get_data(**self.get_active_filter())
            self.updateFromDict(data)
