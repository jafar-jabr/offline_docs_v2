from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QButtonGroup, QRadioButton

from src.Elements.ClickableLabel import ClickableLabel
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.dbSelector import DatabaseSelector
from src.Elements.regularCompoBox import RegularCompoBox
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.remoteDatabase import RemoteDatabase


class CategoryImportModal(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('resources/assets/images/logo.png'))
        self.setObjectName("create_account_modal")
        self.line_width = 480
        self.result = "Not Done"
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 50)  # (left, top, right, bottom)
        nameLabel = RegularLabel('Import Categories')
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
        self.setWindowTitle("Import Categories")
        self.resize(600, 270)
        self.setLayout(self.layout)

    def do_import(self):
        version = self.version_select.currentText()
        db_path = self.db_select.value()
        db_extension = db_path.split(".")[-1]
        if version == "V2":
            MessageBoxes.warning_message("Not Available", "importing from version 2 is not available yet.")
            return
        if db_extension != "db":
            MessageBoxes.warning_message("Not Database", "Please choose target database file.")
            return
        db = RemoteDatabase(db_path)
        remote_cat = db.get_all_categories()
        user_id = SessionWrapper.user_id
        local_cat = Database().get_all_categories(user_id)
        SharedFunctions.import_cats(local_cat, remote_cat, user_id)
        MessageBoxes.success_message("Imported", "Import categories Done")
        self.result = "Done"
        self.accept()
