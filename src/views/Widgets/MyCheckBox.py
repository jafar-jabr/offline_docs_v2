from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QCheckBox

from src.models.SessionWrapper import SessionWrapper


class CheckBox(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        style = """
               QCheckBox{
                   font-size: %s;
                   color: %s;
               }
               QCheckBox::indicator {
                 width: 20px;
                 height: 20px;
               }
               QCheckBox::indicator:unchecked {
                   image: url(./resources/assets/images/checkbox/unchecked.png);
               }
               QCheckBox::indicator:unchecked:pressed {
                    image: url(./resources/assets/images/checkbox/unchecked-pressed);
                }
                
                QCheckBox::indicator:checked {
                    image: url(./resources/assets/images/checkbox/checked.png);
                }
                QCheckBox::indicator:checked:pressed {
                    image: url(./resources/assets/images/checkbox/checked-pressed.png);
                }
                QCheckBox::indicator:indeterminate:pressed {
                    image: url(./resources/assets/images/checkbox/checked.png);
                }
                QCheckBox::indicator:unchecked:hover {
                    image: url(./resources/assets/images/checkbox/unchecked-hover.png);
                }
                QCheckBox::indicator:checked:hover {
                    image: url(./resources/assets/images/checkbox/checked-hover.png);
                }
                QCheckBox::indicator:indeterminate:hover {
                    image: url(./resources/assets/images/checkbox/checked-hover-indeterminate.png);
                }
            """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.setStyleSheet(style)
