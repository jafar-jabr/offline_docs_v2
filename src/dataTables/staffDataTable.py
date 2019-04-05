from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QAbstractItemView
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.CustomLabel import CustomLabel, RegularLabel
from src.Elements.FilterTextBoxAR import FilterTextBoxAR
from src.Elements.MessageBoxes import MessageBoxes
from src.modals.editStaffModal import EditStaffModal
from src.modals.staffDetailModal import StaffDetailModal
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class StaffDataTable(QWidget):
    def __init__(self, grand_father, *args):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.table_width = SessionWrapper.get_dimension('staff_table_w')
        self.current_page = 1
        self.per_page = 10
        self.grand_father = grand_father
        self.clinic_id = SessionWrapper.clinic_id
        self.staff_table = QTableWidget()
        self.staff_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.total_users = 0
        self.setMaximumHeight(int(self.pc_height*0.50))
        data, self.total_pages, self.total_users = self.get_data()
        self.current_label = CustomLabel(str(self.current_page)+" من "+str(self.total_pages))
        self.setmydata(data)
        header_stylesheet = "::section{Background-color:#99d8ff; height: 40px; font-size: 18px; }"
        self.staff_table.horizontalHeader().setStyleSheet(header_stylesheet)
        number_stylesheet = "::section{Background-color:#99d8ff; }"
        self.staff_table.verticalHeader().setStyleSheet(number_stylesheet)
        main_staff_layout = QVBoxLayout()
        main_staff_layout.setContentsMargins(int(self.pc_width*0.18), 0, 0, 50)  # (left, top, right, bottom)
        main_staff_layout.setSpacing(10)
        label_and_searchH = QHBoxLayout()
        self.search_input = FilterTextBoxAR(260, False, "resources/assets/images/search.png", "البحث")
        self.search_input.iconClicked.connect(self.do_search)
        self.all_staff_label = RegularLabel("كل المنتسبين : " + str(self.total_users))
        label_and_searchH.addWidget(self.all_staff_label)
        label_and_searchH.addSpacing(int(self.pc_width*0.45))
        label_and_searchH.addWidget(self.search_input)
        label_and_searchQ = QWidget()
        # label_and_searchQ.setFixedWidth(1355)
        label_and_searchQ.setLayout(label_and_searchH)

        main_staff_layout.addWidget(label_and_searchQ)
        main_staff_layout.addWidget(self.staff_table)
        pagination = self.create_pagination()
        main_staff_layout.addLayout(pagination)
        # main_staff_layout.set
        self.setLayout(main_staff_layout)

    def updateFromDict(self, data):
        self.staff_table.clear()
        self.staff_table.clearContents()
        self.setmydata(data)
        self.current_label.setText(str(self.current_page) + " من " + str(self.total_pages))
        self.all_staff_label.setText("كل المنتسبين : " + str(self.total_users))

    def setmydata(self, data):
        headers = ["اسم المنتسب", "العنوان الوظيفي", "رقم الهاتف", "الصلاحيات", "تاريخ التسجيل", "اخرى"]
        self.staff_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.staff_table.setRowCount(len(data))
        self.staff_table.setColumnCount(len(headers))
        self.staff_table.setColumnWidth(0, self.table_width*0.25)
        self.staff_table.setColumnWidth(1, self.table_width*0.18)
        self.staff_table.setColumnWidth(2, self.table_width*0.13)
        self.staff_table.setColumnWidth(3, self.table_width*0.13)
        self.staff_table.setColumnWidth(4, self.table_width*0.18)
        self.staff_table.setColumnWidth(5, self.table_width*0.13)
        self.staff_table.setHorizontalHeaderLabels(headers)

        self.staff_table.setVerticalHeaderLabels([" "+str(i+1+((self.current_page-1)*self.per_page))+" " for i, row in enumerate(data)])
        for row_index, row in enumerate(data):
            for column_index, cell in enumerate(row):
                cell = str(cell)
                if column_index == len(headers)-1:
                    if SharedFunctions.is_manager():
                        btn1 = ClickableIcon(25, 25, 'resources/assets/images/edit-icon-blue11.png')
                    else:
                        btn1 = ClickableIcon(25, 25, 'resources/assets/images/seemore-icon-circle.png')
                    btn1.setObjectName(cell)
                    btn1.clicked.connect(self.view_or_edit)
                    btn2 = ClickableIcon(25, 25, 'resources/assets/images/delete-icon-blue10.png')
                    btn2.setObjectName(cell)
                    btn2.clicked.connect(self.delete_staff)
                    btn_layout = QHBoxLayout()
                    btn_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
                    btn_layout.addWidget(btn1)
                    btn_layout.addWidget(btn2)
                    container = QWidget()
                    container.setLayout(btn_layout)
                    self.staff_table.setCellWidget(row_index, column_index, container)
                elif column_index == len(headers)-3:
                    # role
                    role_id = int(cell)
                    role = SessionWrapper.all_the_roles[role_id]
                    self.staff_table.setItem(row_index, column_index, QTableWidgetItem(role))
                elif column_index == len(headers)-5:
                    job_id = int(cell)
                    job = SessionWrapper.all_the_jobs[job_id]
                    self.staff_table.setItem(row_index, column_index, QTableWidgetItem(job))
                else:
                    c_cell = SharedFunctions.maybeLongString(cell)
                    self.staff_table.setItem(row_index, column_index, QTableWidgetItem(c_cell))

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

    def get_data(self, search=""):
        return Database().select_all_staff(self.clinic_id, self.current_page, self.per_page, search)

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
        search = self.search_input.text()
        data, self.total_pages, self.total_users = self.get_data(search)
        self.updateFromDict(data)

    def do_search(self):
        search = self.search_input.text()
        self.current_page = 1
        data, self.total_pages, self.total_users = self.get_data(search)
        self.updateFromDict(data)

    def refresh_data(self):
        search = ""
        data, self.total_pages, self.total_users = self.get_data(search)
        self.updateFromDict(data)

    def delete_staff(self):
        staff_id = self.sender().objectName()
        if int(staff_id) == int(SessionWrapper.user_id):
            MessageBoxes.warning_message("خطأ", "لا يمكنك حذف حسابك")
            return
        elif not SharedFunctions.is_manager():
            MessageBoxes.warning_message("خطأ", "ليس لديك الصلاحية للقيام بذلك")
            return
        txt = "هل انت متأكد من رغبتك بحذف كل بيانات هذا المنتسب ؟"
        confirm = MessageBoxes.confirm_message(txt)
        if confirm:
            clinic_id = SessionWrapper.clinic_id
            doctor_count = Database().count_clinic_doctors(clinic_id)
            if doctor_count == 1 and Database().is_doctor(clinic_id, staff_id):
                MessageBoxes.warning_message("غير ممكن!", "لا يمكن حذف الطبيب الوحيد في التطبيق")
                return
            count = Database().count_staff_visits(staff_id)
            if count > 0:
                if count > 1:
                    MessageBoxes.warning_message("غير ممكن!", "لا يمكن حذف الطبيب لانه مرتبط بـ"+str(count)+" مراجعات. ")
                else:
                    MessageBoxes.warning_message("غير ممكن!", "لا يمكن حذف الطبيب لانه مرتبط باحد المراجعين")
            else:
                # ch = Database().check_if_main_doctor(staff_id)
                # if ch:
                #     MessageBoxes.warning_message("خطأ", "لا يمكن حذف الطبيب لانه الطبيب الرئيسي لبعض مستخدمي التطبيق")
                #     return
                Database().delete_staff(staff_id)
                self.refresh_data()

    def view_or_edit(self):
        if SharedFunctions.is_manager():
            staff_id = self.sender().objectName()
            try_edit = EditStaffModal(staff_id)
            if try_edit.status == "Done":
                self.refresh_data()
        else:
            staff_id = self.sender().objectName()
            StaffDetailModal(staff_id)
