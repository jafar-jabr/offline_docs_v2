from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QComboBox, QCompleter


class RegularCompoBox(QComboBox):
    def __init__(self,  options=[], **kwargs):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(False)
        self.setFixedHeight(37)
        model = QStandardItemModel()
        for i, word in enumerate(options):
            item = QStandardItem(word)
            model.setItem(i, 0, item)
        self.setModel(model)
        self.setModelColumn(0)
        if "width" in kwargs:
            self.setFixedWidth(kwargs["width"])
        else:
            self.setFixedWidth(237)

        style = """
        QComboBox {
          border-radius: 10px;
        }
        
        QComboBox::drop-down:button{
            width: 25px;
            
            border-image: url(./resources/assets/images/drop_down.png);
            border-bottom-left-radius: 10px;
            border-top-left-radius: 10px;
        }
        
        QComboBox::drop-down:button:hover{
            
        }
        """
        # background-color: #f5f5f5; background-color: #f5f5f5;
        self.setStyleSheet(style)

    def setModel(self, model):
        super(RegularCompoBox, self).setModel(model)

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)
