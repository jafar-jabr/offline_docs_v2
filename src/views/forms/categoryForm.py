from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog
from PyQt5.QtCore import Qt

from src.views.widgets.ClickableIcon import ClickableIcon
from src.views.widgets.ClickableLabel import ActiveLabel, ClickableLabel
from src.views.widgets.FilterTextBox import FilterTextBox
from src.views.widgets.LabeledTextArea import LabeledTextArea
from src.views.widgets.LabeledTextBox import LabeledTextBox
from src.views.widgets.MessageBoxes import MessageBoxes
from src.views.widgets.iconedClicklableLabel import IconedClickableLabel
from src.views.widgets.myListWidget import MyListWidget
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.GenericFunctions import SharedFunctions
from src.views.modals.dataImportModal import DataImportModal


class CategoryForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("category_page")
        self.parent = parent
        user_id = SessionWrapper.user_id
        categories = Database().get_all_categories(user_id)
        self.categories_by_id, self.categories_by_name = SharedFunctions().format_categories(categories)
        self.selected_cat_id = 0
        self.selected_cat_name = ""
        self.landing_layout = QHBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.landing_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def initUI(self):
        left_widget = QWidget()
        left_widget.setFixedWidth(300)
        lef_column = QVBoxLayout()
        left_widget.setLayout(lef_column)
        lef_column.setContentsMargins(20, 20, 20, 20)  # (left, top, right, bottom)
        self.search_input = FilterTextBox(260, False, "resources/assets/images/search.png", "Search")
        self.search_input.textChanged.connect(self.do_search)
        self.search_input.iconClicked.connect(self.do_search)

        import_label = IconedClickableLabel("Import Data", 260)
        import_label.clicked.connect(self.start_import)

        lef_column.addWidget(import_label)
        lef_column.addWidget(self.search_input)

        left_inner_widget = QWidget()
        left_inner_widget.setFixedWidth(260)
        left_inner_column = QVBoxLayout()
        left_inner_column.setContentsMargins(0, 10, 0, 0)  # (left, top, right, bottom)
        left_inner_column.setSpacing(0)

        left_inner_widget.setLayout(left_inner_column)
        tabs_line = QHBoxLayout()

        categories_tab = ActiveLabel("Categories")
        categories_tab.clicked.connect(lambda: self.go_to_page('categories'))

        documents_tab = ClickableLabel("Documents")
        documents_tab.clicked.connect(lambda: self.go_to_page('documents', selected_cat_id = self.selected_cat_id, selected_cat_name = self.selected_cat_name))

        tabs_line.addWidget(categories_tab)
        tabs_line.addWidget(documents_tab)
        left_inner_column.addLayout(tabs_line)
        categories_options = []
        for opt in self.categories_by_name:
            categories_options.append(opt)
        self.categories_list = MyListWidget(400, 260, options=categories_options)
        self.categories_list.listRightClicked.connect(self.delete_cat)
        self.categories_list.clicked[str].connect(self.category_selected)
        self.categories_list.double_clicked[str].connect(self.cat_double_clicked)
        left_inner_column.addWidget(self.categories_list)
        lef_column.addWidget(left_inner_widget)

        left_widget.setObjectName("categories_left")
        right_column = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setObjectName("category_right")
        right_widget.setFixedWidth(1000)
        right_content = QVBoxLayout()

        add_line = QHBoxLayout()

        add_line.setContentsMargins(0, 20, 50, 0)
        add_line.setSpacing(40)
        self.buttonAddCat = ClickableLabel("Add category", bg_color="#445566")
        self.buttonAddCat.clicked.connect(self.reset_inputs)
        self.buttonAddCat.setObjectName("buttonAddCat")
        self.buttonAddCat.setFixedWidth(125)
        self.buttonAddCat.setAlignment(Qt.AlignCenter)
        add_line.addWidget(self.buttonAddCat)

        right_content.addLayout(add_line)

        self.category_name = LabeledTextBox("Category Name: ", width=500)
        self.category_desc = LabeledTextArea("Description: ", height=150, space=25, width=500)
        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(10)
        buttons_line.setContentsMargins(400, 20, 330, 280) # (left, top, right, bottom)
        update_btn = ClickableIcon(50, 40, "./resources/assets/images/Categories/save-button.png", "Update")
        update_btn.clicked.connect(self.update_or_add_cat)
        buttons_line.addWidget(update_btn)
        right_content.addWidget(self.category_name)
        right_content.addWidget(self.category_desc)
        right_content.addLayout(buttons_line)
        right_widget.setLayout(right_content)
        right_column.addWidget(right_widget)
        self.landing_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        right_content.setContentsMargins(150, 100, 0, 0)  # (left, top, right, bottom)
        self.landing_layout.addWidget(left_widget)
        self.landing_layout.addLayout(right_column)
        self.setLayout(self.landing_layout)
        self.category_name.setText("")
        # self.setS

    def go_to_page(self, which, **kwargs):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to(which, **kwargs)

    def category_selected(self, which):
        self.selected_cat_id = self.categories_by_name[which]['id']
        self.selected_cat_name = which
        desc = self.categories_by_name[which]['desc']
        self.category_name.setText(which)
        self.category_desc.setText(desc)

    def cat_double_clicked(self, which):
        self.selected_cat_id = self.categories_by_name[which]['id']
        self.go_to_page('documents', selected_cat_id=self.selected_cat_id, selected_cat_name=which)

    def start_import(self):
        imp = DataImportModal()
        imp_ex = imp.exec_()
        if imp_ex == QDialog.Accepted and imp.result == "Done":
            self.refresh_data()

    def do_search(self):
        user_id = SessionWrapper.user_id
        search = self.search_input.text()
        cats = Database().get_categories_where(user_id, search)
        self.refresh_data(cats)

    def update_or_add_cat(self):
        cat_id = self.selected_cat_id
        cat_name = self.category_name.text()
        cat_desc = self.category_desc.text()
        user_id = SessionWrapper.user_id
        current_dat = SharedFunctions.get_current_date_str()
        if cat_id:
            Database().update_cat(cat_id, cat_name, cat_desc, current_dat)
            MessageBoxes.success_message("Done", "Category Updated")
            self.refresh_data()
        else:
            if len(cat_name) >= 2:
                cat_id = Database().insert_cat(cat_name, cat_desc, user_id, current_dat)
                MessageBoxes.success_message("Done", "Category saved")
                self.selected_cat_id = cat_id
                self.selected_cat_name = cat_name
                self.refresh_data()
            else:
                MessageBoxes.warning_message("invalid", "Category name can not be less than two characters")

    def delete_cat(self, cat_name):
        ask = MessageBoxes.confirm_message("Are you sure to delete this category and all the documents under it ?")
        if ask:
            cat_id = self.categories_by_name[cat_name]['id']
            SharedFunctions.delete_cat(cat_id)
            self.refresh_data()

    def reset_inputs(self):
        self.selected_cat_id = 0
        self.selected_cat_name = ""
        self.category_name.setText("")
        self.category_desc.setText("")

    def refresh_data(self, data=None):
        if data is None:
            user_id = SessionWrapper.user_id
            data = Database().get_all_categories(user_id)
        self.categories_by_id, self.categories_by_name = SharedFunctions().format_categories(data)
        categories_options = []
        for opt in self.categories_by_name:
            categories_options.append(opt)
        self.categories_list.only_update_options(categories_options)
        self.reset_inputs()
