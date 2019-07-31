from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFormLayout
from src.views.widgets.ClickableIcon import ClickableIcon
from src.views.widgets.CustomLabel import RegularLabel
from src.views.widgets.DateFilterWidget import DateFilterWidget
from src.views.widgets.draggableTextArea import DraggableTextArea
from src.models.DatabaseModel import Database
from src.models.SessionWrapper import SessionWrapper
from PyQt5.QtCore import QRect
from src.models.GenericFunctions import SharedFunctions


class StickyNotesForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.create_table_if_needed()
        self.setObjectName("sticky_notes_page")
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.sticky_layout = QFormLayout(self)
        self.sticky_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.sticky_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        if 'date' in kwargs:
            the_date = kwargs['date']
        else:
            the_date = None
        self.initUI(the_date)

    def initUI(self, the_date):
        if the_date is not None:
            self.date_select = DateFilterWidget(0, 10, value=the_date)
        else:
            self.date_select = DateFilterWidget(0, 10)
            the_date = self.date_select.value()
        exist_notes = Database().get_notes_by_date(the_date)
        self.date_select.clicked.connect(self.date_changed)
        for note in exist_notes:
            test_input_1 = DraggableTextArea(self)
            test_input_1.setObjectName(str(note['id']))
            test_input_1.setText(note['details'])
            test_input_1.moved.connect(self.note_moved)
            test_input_1.lost_focus.connect(self.note_lost_focus)
            # test_input_1.setGeometry(QRect(320, self.y() + 200, 300, 45))  # (x, y, width, height)
            test_input_1.setGeometry(QRect(note['x_pos'], note['y_pos'], note['the_width'], note['the_height']))  # (x, y, width, height)
        lbl = RegularLabel("Inspired by windows 10 sticky notes")
        self.sticky_layout.addWidget(lbl)
        action_line = QHBoxLayout()
        add_note_btn = ClickableIcon(50, 40, "./resources/assets/images/add_icon.png", "Add")
        add_note_btn.clicked.connect(self.add_new_note)
        action_line.addWidget(self.date_select)
        action_line.addWidget(add_note_btn)
        action_widget = QWidget()
        action_widget.setFixedWidth(300)
        action_widget.setLayout(action_line)
        self.sticky_layout.addWidget(action_widget)
        self.sticky_layout.setAlignment(Qt.AlignTop)

    def add_new_note(self):
        note_date=self.date_select.value()
        note_details=""
        current_date = SharedFunctions.get_current_date_str()
        the_new_note = Database().insert_note(note_date, note_details, current_date)
        test_input = DraggableTextArea(self)
        test_input.setObjectName(str(the_new_note))
        test_input.setGeometry(QRect(400, self.y() + 250, 300, 45))  # (x, y, width, height)
        test_input.setParent(None)
        self.layout().addChildWidget(test_input)
        test_input.moved.connect(self.note_moved)
        test_input.lost_focus.connect(self.note_lost_focus)

    def note_moved(self):
        note_id = self.sender().objectName()
        x_pos = self.sender().x()
        y_pos = self.sender().y()
        current_date = SharedFunctions.get_current_date_str()
        Database().update_note_pos(note_id, x_pos, y_pos, current_date)

    def note_lost_focus(self):
        note_id = self.sender().objectName()
        note_details = self.sender().toPlainText()
        current_date = SharedFunctions.get_current_date_str()
        Database().update_note_details(note_id, note_details, current_date)

    def date_changed(self):
        new_date = self.sender().value()
        self.reload_page(new_date)

    def reload_page(self, date):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to('sticky_notes', date=date)

    def create_table_if_needed(self):
        create_query = """ 
                CREATE TABLE "sticky_notes" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"note_date"	DATETIME,
	"details"	TEXT NOT NULL,
	"x_pos"	INTEGER NOT NULL DEFAULT 400,
	"y_pos"	INTEGER NOT NULL DEFAULT 250,
	"the_width"	INTEGER NOT NULL DEFAULT 200,
	"the_height"	INTEGER NOT NULL DEFAULT 300,
	"created_at"	DATETIME NOT NULL,
	"updated_at"	DATETIME
);"""
        Database().create_table_if_not_exist('sticky_notes', create_query)
