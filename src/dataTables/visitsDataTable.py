from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QSizePolicy, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, \
    QAbstractItemView
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.CustomLabel import CustomLabel
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class VisitsDataTable(QWidget):
    def __init__(self, grand_father, patient_id, *args):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.current_page = 1
        self.per_page = 5
        self.grand_father = grand_father
        self.patient_id = patient_id
        self.clinic_id = SessionWrapper.clinic_id
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.table.setFixedHeight(200)
        self.table.setFixedWidth(self.pc_width)
        data, self.total_pages = self.get_data()
        self.current_label = CustomLabel(str(self.current_page)+" من "+str(self.total_pages))
        self.setmydata(data)
        header_stylesheet = "::section{Background-color:#99d8ff; height: 40px; font-size: 18px; }"
        self.table.horizontalHeader().setStyleSheet(header_stylesheet)
        number_stylesheet = "::section{Background-color:#99d8ff; }"
        self.table.verticalHeader().setStyleSheet(number_stylesheet)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 10)  # (left, top, right, bottom)
        main_layout.setSpacing(5)
        main_layout.addWidget(self.table)
        pagination = self.create_pagination()
        main_layout.addLayout(pagination)
        self.setLayout(main_layout)

    def updateFromDict(self, data):
        self.table.clear()
        self.table.clearContents()
        self.setmydata(data)
        self.current_label.setText(str(self.current_page) + " من " + str(self.total_pages))

    def setmydata(self, data):
        table_width = SessionWrapper.get_dimension('all_visits_table_w')
        headers = ["الاعراض", "التشخيص", "التوصيات", "تاريخ المراجعة",  "الطبيب",
                       "حالة المراجعة", "اخرى"]
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setColumnWidth(0, table_width*0.25)
        self.table.setColumnWidth(1, table_width*0.15)
        self.table.setColumnWidth(2, table_width*0.22)
        self.table.setColumnWidth(3, table_width*0.10)
        self.table.setColumnWidth(4, table_width*0.10)
        self.table.setColumnWidth(5, table_width*0.10)
        self.table.setColumnWidth(6, table_width*0.08)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels([" "+str(i+1+((self.current_page-1)*self.per_page))+" " for i, row in enumerate(data)])
        for row_index, row in enumerate(data):
            for column_index, cell in enumerate(row):
                cell = str(cell)
                if column_index == len(headers)-1:
                    btn = ClickableIcon(25, 25, 'resources/assets/images/seemore-icon-circle.png')
                    btn.setObjectName(cell)
                    btn.clicked.connect(self.details_clicked)

                    btn_layout = QHBoxLayout()
                    btn_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
                    btn_layout.addWidget(btn)
                    container = QWidget()
                    container.setLayout(btn_layout)

                    self.table.setCellWidget(row_index, column_index, container)
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

    def get_data(self):
        return Database().select_other_visits(self.patient_id, self.current_page, self.per_page)

    def do_pagination(self, direction):
        if direction == "last":
            self.current_page = self.total_pages
        elif direction == "first":
            self.current_page = 1
        elif direction == "down":
            self.current_page = self.current_page -1
            if self.current_page <= 0:
                self.current_page = 1
        elif direction == "up":
            self.current_page = self.current_page + 1
            if self.current_page > self.total_pages:
                self.current_page = self.total_pages
        data, self.total_pages = self.get_data()
        self.updateFromDict(data)

    def refresh_data(self):
        self.current_page = 1
        data, self.total_pages = self.get_data()
        self.updateFromDict(data)
