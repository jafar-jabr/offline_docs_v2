from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFrame
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.ClickableLabel import ClickableLabel, ActiveLabel
from src.Elements.FilterTextBox import FilterTextBox
from src.Elements.LabeledTextArea import LabeledTextArea
from src.Elements.LabeledTextBox import LabeledTextBox
from src.Elements.myListWidget import MyListWidget
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class CategoryForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("category_page")
        self.parent = parent
        user_id = SessionWrapper.user_id
        categories = Database().get_all_categories(user_id)
        default_cat = Database().get_default_cat(user_id)
        self.categories_by_id, self.categories_by_name = SharedFunctions().format_categories(categories)
        self.selected_cat_id = default_cat['id']
        self.selected_cat_name = default_cat['cat_name']
        self.pages_count = 6
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
        search_input = FilterTextBox(260, False, "resources/assets/images/search.png", "Search")
        lef_column.addWidget(search_input)

        left_inner_widget = QWidget()
        left_inner_widget.setFixedWidth(260)
        left_inner_column = QVBoxLayout()
        left_inner_column.setContentsMargins(0, 50, 0, 0)  # (left, top, right, bottom)
        left_inner_column.setSpacing(0)

        left_inner_widget.setLayout(left_inner_column)
        tabs_line = QHBoxLayout()

        categories_tab = ActiveLabel("Categories")
        categories_tab.clicked.connect(lambda: self.go_to_page('categories'))

        documents_tab = ClickableLabel("Documents")
        documents_tab.clicked.connect(lambda: self.go_to_page('documents', categories_by_name=self.categories_by_name, categories_by_id = self.categories_by_id, selected_cat_id = self.selected_cat_id, selected_cat_name = self.selected_cat_name))

        tabs_line.addWidget(categories_tab)
        tabs_line.addWidget(documents_tab)
        left_inner_column.addLayout(tabs_line)
        categories_options = []
        for opt in self.categories_by_name:
            categories_options.append(opt)

        categories_list = MyListWidget(500, 260, options=categories_options)
        categories_list.clicked[str].connect(self.category_selected)
        left_inner_column.addWidget(categories_list)
        lef_column.addWidget(left_inner_widget)
        left_widget.setObjectName("categories_left")
        right_column = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setObjectName("category_right")
        right_widget.setFixedWidth(1000)
        right_content = QVBoxLayout()
        self.category_name = LabeledTextBox("Category Name: ", width=500)
        self.category_desc = LabeledTextArea("Description: ", height=150, space=25, width=500)
        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(10)
        buttons_line.setContentsMargins(370, 20, 330, 280) # (left, top, right, bottom)
        save_btn = ClickableIcon(50, 40, "./resources/assets/images/Categories/save-button.png", "Update")
        delete_btn = ClickableIcon(40, 40, "./resources/assets/images/Categories/delete-button.png", "Delete")
        buttons_line.addWidget(save_btn)
        buttons_line.addWidget(delete_btn)
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
