from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout
from src.views.widgets.ClickableIcon import ClickableIcon
from src.views.widgets.LabeledTextArea import LabeledTextArea
from src.views.widgets.LabeledTextBox import LabeledTextBox
from src.views.widgets.MessageBoxes import MessageBoxes
from src.views.widgets.regularCompoBox import RegularCompoBox
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper


class AddDocumentModal(QDialog):
    def __init__(self, cat_id):
        super().__init__()
        title = "Add Document"
        self.cat_id = cat_id
        self.result = "try"
        self.inner_width = SessionWrapper.get_dimension('main_inner_w')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.setWindowIcon(QIcon('resources/assets/images/icon.ico'))
        self.setObjectName("full_text")
        self.docs_layout = QHBoxLayout()
        self.docs_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, main, bottom)
        self.docs_layout.setSpacing(0)
        main_column = QVBoxLayout()
        main_widget = QWidget()
        main_widget.setObjectName("category_main")
        main_widget.setFixedWidth(self.inner_width)
        main_content = QVBoxLayout()
        cat_options = SessionWrapper.documents_types
        self.doc_type_select = RegularCompoBox(cat_options)

        self.document_name = LabeledTextBox("Name:       ", width=400)
        self.document_desc = LabeledTextArea("Details: ", height=400, space=25, width=700)
        self.document_tags = LabeledTextArea("Tags:    ", height=100, space=25, width=700)

        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(10)
        buttons_line.setContentsMargins(400, 20, 330, 20)  # (left, top, main, bottom)
        save_btn = ClickableIcon(50, 50, "./resources/assets/images/Categories/save-button.png", "Update")
        save_btn.clicked.connect(self.do_save)

        buttons_line.addWidget(save_btn)

        main_content.addWidget(self.doc_type_select)
        main_content.addWidget(self.document_name)
        main_content.addWidget(self.document_desc)
        main_content.addWidget(self.document_tags)
        main_content.addLayout(buttons_line)
        main_widget.setLayout(main_content)
        main_column.addWidget(main_widget)
        self.docs_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, main, bottom)
        main_content.setContentsMargins(50, 20, 0, 0)  # (left, top, main, bottom)
        self.docs_layout.addLayout(main_column)
        self.setLayout(self.docs_layout)
        self.setWindowTitle(title)

    def do_save(self):
        doc_type = self.doc_type_select.currentText()
        doc_name = self.document_name.text()
        doc_details = self.document_desc.text()
        doc_tags = self.document_tags.text()
        if doc_type != "Normal":
            msg = "adding %s documents is not available yet" % doc_type
            MessageBoxes.warning_message("Not Available", msg)
        else:
            doc_id = Database().insert_doc(self.cat_id, doc_name, doc_details, doc_type)
            Database().insert_tags(doc_tags, doc_id)
            MessageBoxes.success_message("Done", "Document Saved")
            self.result = "Done"
            self.accept()