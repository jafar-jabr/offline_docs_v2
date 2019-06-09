from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFrame
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.ClickableLabel import ClickableLabel, ActiveLabel
from src.Elements.FilterTextBox import FilterTextBox
from src.Elements.LabeledTextArea import LabeledTextArea
from src.Elements.LabeledTextBox import LabeledTextBox
from src.Elements.filteredCompoBox import FilteredComboBox
from src.Elements.iconedClicklableLabel import IconedClickableLabel
from src.Elements.myListWidget import MyListWidget
from src.modals.docImportModal import DocumentImportModal
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class DocumentsForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("documents_page")
        self.parent = parent
        self.categories_by_name = kwargs['categories_by_name']
        self.categories_by_id = kwargs['categories_by_id']
        self.selected_cat_id = kwargs['selected_cat_id']
        self.selected_cat_name = kwargs['selected_cat_name']
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
        lef_column.setContentsMargins(20, 20, 20, 50)  # (left, top, right, bottom)
        cat_options = []
        for cat in self.categories_by_name:
            cat_options.append(cat)
        category_select = FilteredComboBox(cat_options)
        category_select.activated[str].connect(self.category_changed)
        if self.selected_cat_id:
            category_select.setCurrentText(self.selected_cat_name)
        search_input2 = FilterTextBox(260, False, "resources/assets/images/search.png", "Search")
        lef_column.addWidget(category_select)
        lef_column.addWidget(search_input2)

        left_inner_widget = QWidget()
        left_inner_widget.setFixedWidth(260)
        left_inner_column = QVBoxLayout()
        left_inner_column.setContentsMargins(0, 50, 0, 0)  # (left, top, right, bottom)
        left_inner_column.setSpacing(0)

        left_inner_widget.setLayout(left_inner_column)
        tabs_line = QHBoxLayout()

        categories_tab = ClickableLabel("Categories")
        categories_tab.clicked.connect(lambda: self.go_to_page('categories'))

        documents_tab = ActiveLabel("Documents")
        documents_tab.clicked.connect(lambda: self.go_to_page('documents'))

        tabs_line.addWidget(categories_tab)
        tabs_line.addWidget(documents_tab)
        left_inner_column.addLayout(tabs_line)

        docs = Database().get_docs_for_category(self.selected_cat_id)
        docs_options = []
        for opt in docs:
            docs_options.append(opt['doc_name'])
        self.documents_list = MyListWidget(450, 260, options=docs_options)
        self.documents_list.clicked[str].connect(self.document_selected)
        left_inner_column.addWidget(self.documents_list)
        lef_column.addWidget(left_inner_widget)

        import_label = IconedClickableLabel("Import Documents", 260)
        import_label.clicked.connect(self.start_import)
        lef_column.addWidget(import_label)

        left_widget.setObjectName("categories_left")
        right_column = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setObjectName("category_right")
        right_widget.setFixedWidth(1000)
        right_content = QVBoxLayout()
        self.document_name = LabeledTextBox("Name:       ", width=400)
        self.document_desc = LabeledTextArea("Details: ", height=400, space=25, width=700)
        self.document_tags = LabeledTextArea("Tags:    ", height=100, space=25, width=700)
        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(10)
        buttons_line.setContentsMargins(370, 20, 330, 20) # (left, top, right, bottom)
        save_btn = ClickableIcon(50, 50, "./resources/assets/images/Categories/save-button.png", "Update")
        delete_btn = ClickableIcon(50, 50, "./resources/assets/images/Categories/delete-button.png", "Delete")
        buttons_line.addWidget(save_btn)
        buttons_line.addWidget(delete_btn)
        right_content.addWidget(self.document_name)
        right_content.addWidget(self.document_desc)
        right_content.addWidget(self.document_tags)
        right_content.addLayout(buttons_line)
        right_widget.setLayout(right_content)
        right_column.addWidget(right_widget)
        self.landing_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        right_content.setContentsMargins(50, 20, 0, 0)  # (left, top, right, bottom)
        self.landing_layout.addWidget(left_widget)
        self.landing_layout.addLayout(right_column)
        self.setLayout(self.landing_layout)
        # self.setS

    def go_to_page(self, which):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to(which)

    def document_selected(self, which):
        doc_details = Database().get_doc_details(self.selected_cat_id, which)
        doc_id = doc_details['id']
        doc_tags = Database().get_tags_by_doc(doc_id)
        tags = SharedFunctions.make_tags_text(doc_tags)
        self.document_name.setText(doc_details['doc_name'])
        self.document_desc.setText(doc_details['details'])
        self.document_tags.setText(tags)

    def category_changed(self, cat):
        cat_id = self.categories_by_name[cat]['id']
        docs = Database().get_docs_for_category(cat_id)
        docs_options = []
        for opt in docs:
            docs_options.append(opt['doc_name'])
        self.documents_list.only_update_options(docs_options)
        self.selected_cat_id = cat_id
        self.selected_cat_name = cat

    def start_import(self):
        DocumentImportModal(self.selected_cat_name, self.selected_cat_id)
