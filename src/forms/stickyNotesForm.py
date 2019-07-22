from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.CustomLabel import RegularLabel
from src.Elements.DateFilterWidget import DateFilterWidget
from src.Elements.draggableTextArea import DraggableTextArea
from src.models.SessionWrapper import SessionWrapper
from PyQt5.QtCore import QRect


class StickyNotesForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("sticky_notes_page")
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.sticky_layout = QVBoxLayout(self)
        self.sticky_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.sticky_layout.setSpacing(0)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def initUI(self):
        lbl = RegularLabel("Inspired by windows 10 sticky notes")
        test_input_1 = DraggableTextArea(self)
        self.sticky_layout.addWidget(lbl)
        date_select = DateFilterWidget(0, 10)
        action_line = QHBoxLayout()
        add_note_btn = ClickableIcon(50, 40, "./resources/assets/images/add_icon.png", "Add")
        add_note_btn.clicked.connect(self.add_new_note)
        action_line.addWidget(date_select)
        action_line.addWidget(add_note_btn)
        test_input_1.setGeometry(QRect(320, self.y() + 200, 300, 45))  # (x, y, width, height)
        self.sticky_layout.addLayout(action_line)
        self.sticky_layout.setAlignment(Qt.AlignTop)
        date_select.move(400, 200)

    def add_new_note(self):
        test_input = DraggableTextArea(self)
        test_input.setGeometry(QRect(400, self.y() + 250, 300, 45))  # (x, y, width, height)
        test_input.setParent(None)
        self.layout().addWidget(test_input)
