from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.ClickableLabel import ClickableLabel, ActiveLabel
from src.Elements.FilterTextBox import FilterTextBox
from src.Elements.LabeledTextArea import LabeledTextArea
from src.Elements.LabeledTextBox import LabeledTextBox
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.filteredCompoBox import FilteredComboBox
from src.Elements.myListWidget import MyListWidget
from src.modals.addDocModal import AddDocumentModal
from src.modals.docImportModal import DocumentImportModal
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions


class DocumentsForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("documents_page")
        self.parent = parent
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        user_id = SessionWrapper.user_id
        categories = Database().get_all_categories(user_id)
        self.selected_doc_id = 0
        self.selected_doc_name = ""
        self.categories_by_id, self.categories_by_name = SharedFunctions().format_categories(categories)
        self.selected_cat_id = kwargs['selected_cat_id']
        self.selected_cat_name = kwargs['selected_cat_name']
        if not self.selected_cat_id:
            default_cat = Database().get_default_cat(user_id)
            if default_cat is not None:
                self.selected_cat_id = default_cat['id']
                self.selected_cat_name = default_cat['cat_name']
        self.docs_layout = QHBoxLayout()
        self.docs_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.docs_layout.setSpacing(0)
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
        self.search_input = FilterTextBox(260, False, "resources/assets/images/search.png", "Search")
        self.search_input.textChanged.connect(self.do_search)
        self.search_input.iconClicked.connect(self.do_search)
        lef_column.addWidget(category_select)
        lef_column.addWidget(self.search_input)

        left_inner_widget = QWidget()
        left_inner_widget.setFixedWidth(260)
        left_inner_column = QVBoxLayout()
        left_inner_column.setContentsMargins(0, 20, 0, 0)  # (left, top, right, bottom)
        left_inner_column.setSpacing(0)

        left_inner_widget.setLayout(left_inner_column)
        tabs_line = QHBoxLayout()

        categories_tab = ClickableLabel("Categories")
        categories_tab.clicked.connect(lambda: self.go_to_page('categories'))

        documents_tab = ActiveLabel("Documents +", bg_color="#ffffff", front_color="#445566")
        documents_tab.clicked.connect(self.add_doc)

        tabs_line.addWidget(categories_tab)
        tabs_line.addWidget(documents_tab)
        left_inner_column.addLayout(tabs_line)

        docs = Database().get_docs_for_category(self.selected_cat_id)
        docs_options = []
        for opt in docs:
            docs_options.append(opt['doc_name'])
        self.documents_list = MyListWidget(450, 260, options=docs_options, bg_color="#ffffff", front_color="#445566")
        self.documents_list.listRightClicked.connect(self.delete_doc)
        self.documents_list.clicked[str].connect(self.document_selected)
        left_inner_column.addWidget(self.documents_list)
        lef_column.addWidget(left_inner_widget)

        left_widget.setObjectName("categories_left")

        right_column = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setObjectName("category_right")
        right_widget.setFixedWidth(int(self.pc_width*0.8))
        right_content = QVBoxLayout()
        self.document_name = LabeledTextBox("Name:       ", width=400)

        self.document_desc = LabeledTextArea("Details: ", height=400, space=25, width=self.width()+250)

        self.document_tags = LabeledTextArea("Tags:    ", height=100, space=25, width=self.width()+250)

        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(10)
        buttons_line.setContentsMargins(400, 20, 330, 20) # (left, top, right, bottom)
        update_btn = ClickableIcon(50, 50, "./resources/assets/images/Categories/save-button.png", "Update")
        update_btn.clicked.connect(self.update_doc)

        buttons_line.addWidget(update_btn)
        right_content.addWidget(self.document_name)
        right_content.addWidget(self.document_desc)
        right_content.addWidget(self.document_tags)
        right_content.addLayout(buttons_line)
        right_widget.setLayout(right_content)
        right_column.addWidget(right_widget)
        self.docs_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        right_content.setContentsMargins(10, 20, 0, 0)  # (left, top, right, bottom)
        self.docs_layout.addWidget(left_widget)
        self.docs_layout.addLayout(right_column)
        self.setLayout(self.docs_layout)
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
        self.selected_doc_id = doc_id
        self.selected_doc_name = doc_details['doc_name']

    def category_changed(self, cat):
        cat_id = self.categories_by_name[cat]['id']
        docs = Database().get_docs_for_category(cat_id)
        docs_options = []
        for opt in docs:
            docs_options.append(opt['doc_name'])
        self.documents_list.only_update_options(docs_options)
        self.selected_cat_id = cat_id
        self.selected_cat_name = cat
        self.reset_inputs()

    def start_import(self):
        imp = DocumentImportModal(self.selected_cat_name, self.selected_cat_id)
        imp_ex = imp.exec_()
        if imp_ex == QDialog.Accepted and imp.result == "Done":
            self.refresh_data()

    def do_search(self):
        search = self.search_input.text()
        docs = Database().get_doc_for_category_where(self.selected_cat_id, search)
        self.refresh_data(docs)

    def reset_inputs(self):
        self.selected_doc_id = 0
        self.selected_doc_name = ""
        self.document_name.setText("")
        self.document_desc.setText("")
        self.document_tags.setText("")

    def refresh_data(self, docs=None):
        if docs is None:
            docs = Database().get_docs_for_category(self.selected_cat_id)
        docs_options = []
        for opt in docs:
            docs_options.append(opt['doc_name'])
        self.documents_list.only_update_options(docs_options)
        self.reset_inputs()

    def update_doc(self):
        doc_id = self.selected_doc_id
        if doc_id:
            doc_name = self.document_name.text()
            doc_desc = self.document_desc.text()
            doc_tags = self.document_tags.text()
            Database().update_doc(doc_id, doc_name, doc_desc, doc_tags)
            self.refresh_data()
            self.document_name.setText(doc_name)
            self.document_desc.setText(doc_desc)
            self.document_tags.setText(doc_tags)
            self.selected_doc_id = doc_id
            self.selected_doc_name = doc_name

    def delete_doc(self, doc_name):
        ask = MessageBoxes.confirm_message("Are you sure to delete this Document?")
        if ask:
            doc_details = Database().get_doc_details(self.selected_cat_id, doc_name)
            Database().delete_doc(doc_details['id'])
            self.refresh_data()

    def add_doc(self):
        if not self.selected_cat_id:
            msg = "No category selected"
            MessageBoxes.warning_message("Not Available", msg)
        else:
            imp = AddDocumentModal(self.selected_cat_id)
            imp_ex = imp.exec_()
            if imp_ex == QDialog.Accepted and imp.result == "Done":
                self.refresh_data()
