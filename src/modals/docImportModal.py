from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QButtonGroup, QRadioButton

from src.Elements.ClickableLabel import ClickableLabel
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.dbSelector import DatabaseSelector
from src.Elements.regularCompoBox import RegularCompoBox
from src.models.DatabaseModel import Database
from src.models.SharedFunctions import SharedFunctions
from src.models.remoteDatabase import RemoteDatabase


class DocumentImportModal(QDialog):
    def __init__(self, cat_name, cat_id):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("create_account_modal")
        self.line_width = 480
        self.import_type = "merge" # skip, overwrite
        self.cat_id = cat_id
        self.cat_name = cat_name
        self.layout = QVBoxLayout()
        self.result = "try"
        self.registered_email = ""
        self.registered_password = ""
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        nameLabel = RegularLabel('Import Documents into '+cat_name)
        target_v_H = QHBoxLayout()
        v_label = RegularLabel('Target Version:')
        v_options = ['V1', 'V2']
        self.version_select = RegularCompoBox(v_options)
        target_v_H.addWidget(v_label)
        target_v_H.addWidget(self.version_select)
        db_h = QHBoxLayout()
        codeLabel = RegularLabel('Target Database: ')
        self.db_select = DatabaseSelector()
        db_h.addWidget(codeLabel)
        db_h.addWidget(self.db_select)
        import_options_h = QHBoxLayout()

        self.calculation_options_group = QButtonGroup()  # Number group

        r1 = QRadioButton("Merge exist Documents")
        r1.setChecked(True)
        r1.toggled.connect(lambda: self.set_result_type(r1, "merge"))
        r2 = QRadioButton("Skip exist Documents")
        r2.toggled.connect(lambda: self.set_result_type(r2, "skip"))

        r3 = QRadioButton("Overwrite exist Documents")
        r3.toggled.connect(lambda: self.set_result_type(r3, "overwrite"))

        self.calculation_options_group.addButton(r1)
        self.calculation_options_group.addButton(r2)
        self.calculation_options_group.addButton(r3)

        import_options_h.addWidget(r1)
        import_options_h.addWidget(r2)
        import_options_h.addWidget(r3)

        self.do_import_btn = ClickableLabel("Do Import")
        self.do_import_btn.clicked.connect(self.do_import)
        self.do_import_btn.setObjectName("buttonImport")
        self.do_import_btn.setFixedWidth(150)
        self.do_import_btn.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(nameLabel)
        self.layout.addLayout(target_v_H)
        self.layout.addLayout(db_h)
        self.layout.addLayout(import_options_h)
        self.layout.addWidget(self.do_import_btn)
        self.setWindowTitle("Import Document")
        self.resize(600, 270)
        self.setLayout(self.layout)
        self.exec_()

    def do_import(self):
        version = self.version_select.currentText()
        cat_name = self.cat_name
        cat_id = self.cat_id
        import_type = self.import_type
        db_path = self.db_select.value()
        db_extension = db_path.split(".")[-1]
        if db_extension != "db":
            MessageBoxes.warning_message("Not Database", "Please choose target database file.")
            return
        if version == "V2":
            MessageBoxes.warning_message("Not Available", "importing from version 2 is not available yet.")
            return
        db = RemoteDatabase(db_path)
        remote_docs = db.get_docs_for_category(cat_name)
        local_docs = Database().get_detailed_docs_for_category(cat_id)
        if import_type == "merge":
            SharedFunctions.merge_import_docs(local_docs, remote_docs)
            MessageBoxes.success_message("Imported", "Import documents Done")
            self.accept()
        print(remote_docs)

    def set_result_type(self, instance, import_type):
        if instance.isChecked():
            self.import_type = import_type
