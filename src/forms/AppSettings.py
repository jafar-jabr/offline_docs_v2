from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from src.Elements.CustomLabel import RegularLabel, HeadLineLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.filteredCompoBox import FilteredCombo
from src.Elements.regularCompoBox import RegularCompoBox
from src.models.DatabaseModel import Database
from src.models.SharedFunctions import SharedFunctions
from src.models.SessionWrapper import SessionWrapper
from src.models.UserBlock import UserBlock


class AppSettings(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.clinic_id = SessionWrapper.clinic_id
        self.about_layout = QVBoxLayout()
        self.about_layout.setSpacing(20)
        self.initUI()

    def initUI(self):
        self.line_width = self.pc_width * 0.3
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 30, 80, 20) #(left, top, right, bottom)
        self.user = UserBlock(self)
        self.noteLabel = HeadLineLabel('<p style="padding: 10px; margin: 10px;">بما ان التطبيق يمكن ان يستخدم لادارة بيانات المراجعين لطبيب واحد او عدة اطباء<br>يمكنك اعداد هذا الخيار من هنا <br>')

        first_grid = QGridLayout()
        first_grid.setSpacing(25)
        first_grid.setColumnStretch(5, 1) #column, strech

        self.mode_label = RegularLabel('نمط الاستخدام :')
        mode_options = ['طبيب واحد', 'عدة اطباء']
        self.mode_select = FilteredCombo(mode_options)
        self.mode_select.activated[str].connect(self.mode_changed)

        if SessionWrapper.app_mode == 1:
            self.mode_select.setCurrentText('طبيب واحد')
        else:
            self.mode_select.setCurrentText('عدة اطباء')

        first_grid.addWidget(self.mode_label, 1, 0)  # ( row, column)
        first_grid.addWidget(self.mode_select, 1, 1)

        self.main_doctor_label = RegularLabel('               اسم الطبيب :')
        doctor_options = Database().select_all_doctors(self.clinic_id)
        formatted_doctors_options = SharedFunctions.format_doctors_list(doctor_options, "اختر")
        self.main_doctor_select = FilteredCombo(formatted_doctors_options)
        self.main_doctor_select.setCurrentText("اختر")

        first_grid.addWidget(self.main_doctor_label, 1, 3)  # ( row, column)
        first_grid.addWidget(self.main_doctor_select, 1, 4)

        if SessionWrapper.app_mode == 1:
            main_doctor_name = SharedFunctions.get_main_doctor()
            self.main_doctor_select.setCurrentText(main_doctor_name)
        else:
            self.main_doctor_select.hide()
            self.main_doctor_label.hide()
        self.color_label = RegularLabel('لون الخط :')
        color_options = ["الابيض", "الاسود", "الاحمر", "الازرق"]
        self.color_select = RegularCompoBox(color_options)
        color_code = SessionWrapper.font_color
        color_name = SessionWrapper.code_to_color[color_code]
        self.color_select.setCurrentText(color_name)

        first_grid.addWidget(self.color_label, 2, 0)  # ( row, column)
        first_grid.addWidget(self.color_select, 2, 1)

        self.font_size_label = RegularLabel('               حجم الخط :')
        font_size_options = ["16px", "18px", "20px", "21px", "22px"]
        self.font_size_select = RegularCompoBox(font_size_options)
        size_number = SessionWrapper.regular_size
        size_name = SessionWrapper.number_to_size[size_number]
        self.font_size_select.setCurrentText(size_name)

        first_grid.addWidget(self.font_size_label, 2, 3)  # ( row, column)
        first_grid.addWidget(self.font_size_select, 2, 4)

        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(40, 20, int(self.pc_width*0.4), 20) #(left, top, right, bottom)
        saveBtn = RegularButton('حفظ')
        saveBtn.setMaximumWidth(100)
        saveBtn.clicked.connect(lambda: self.do_save_preferences(
                                                            self.mode_select.currentText(),
                                                            self.main_doctor_select.currentText(),
                                                            self.color_select.currentText(),
                                                            self.font_size_select.currentText()))
        btnLine.addWidget(saveBtn)
        btnLineQ = QWidget()
        btnLineQ.setLayout(btnLine)
        btnLineQ.setFixedWidth(self.pc_width*0.5)
    #
        self.layout.addWidget(self.noteLabel)
        self.layout.addLayout(first_grid)

        self.layout.addWidget(btnLineQ)

        self.shortcuts = HeadLineLabel('الاختصارات:')

        second_grid = QGridLayout()
        second_grid.setContentsMargins(0, 30, 80, 20) #(left, top, right, bottom)
        second_grid.setSpacing(25)
        second_grid.setColumnStretch(2, 4)  # row column

        self.shortcut_1_label = RegularLabel('Ctrl+H')
        self.shortcut_1_desc = RegularLabel('الصفحة الرئيسية')

        second_grid.addWidget(self.shortcut_1_label, 1, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_1_desc, 1, 1)

        self.shortcut_2_label = RegularLabel('Ctrl+N')
        self.shortcut_2_desc = RegularLabel('اضافة مراجع')

        second_grid.addWidget(self.shortcut_2_label, 2, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_2_desc, 2, 1)

        self.shortcut_3_label = RegularLabel('Ctrl+S')
        self.shortcut_3_desc = RegularLabel('اعدادات المؤسسة والكادر')

        second_grid.addWidget(self.shortcut_3_label, 3, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_3_desc, 3, 1)

        self.shortcut_4_label = RegularLabel('Ctrl+M')
        self.shortcut_4_desc = RegularLabel('اعدادات الحساب')

        second_grid.addWidget(self.shortcut_4_label, 4, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_4_desc, 4, 1)

        self.shortcut_5_label = RegularLabel('Ctrl+T')
        self.shortcut_5_desc = RegularLabel('الاتصال بنا')

        second_grid.addWidget(self.shortcut_5_label, 5, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_5_desc, 5, 1)

        self.shortcut_6_label = RegularLabel('Ctrl+G')
        self.shortcut_6_desc = RegularLabel('اعدادات التطبيق')

        second_grid.addWidget(self.shortcut_6_label, 6, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_6_desc, 6, 1)

        self.shortcut_7_label = RegularLabel('Ctrl+O')
        self.shortcut_7_desc = RegularLabel('حول')

        second_grid.addWidget(self.shortcut_7_label, 7, 0)  # ( row, column)
        second_grid.addWidget(self.shortcut_7_desc, 7, 1)

        self.layout.addWidget(self.shortcuts)
        self.layout.addLayout(second_grid)
        self.setLayout(self.layout)

    def do_save_preferences(self, the_mode, main_doctor, font_color, regular_label_size):
        big_label_size = str(int(regular_label_size[:2])+2)+'px'
        user_id = SessionWrapper.user_id
        app_mode = 0
        main_doctor_id = 0
        if the_mode == "طبيب واحد":
            if main_doctor == "اختر":
                MessageBoxes.warning_message("خطأ", "اسم الطبيب مطلوب")
                return
            doctor_id = Database().get_doctor_id(main_doctor)
            if doctor_id == 0:
                MessageBoxes.warning_message("خطأ", "اسم الطبيب غير موجود")
                return
            app_mode = 1
            main_doctor_id = doctor_id
        else:
            clinic_id = SessionWrapper.clinic_id
            doctor_count = Database().count_clinic_doctors(clinic_id)
            if doctor_count == 1:
                MessageBoxes.warning_message("خطأ", "ليس هناك اكثر من طبيب واحد")
                return
        font_color_r = SessionWrapper.color_to_code[font_color]
        font_size_r = SessionWrapper.size_to_number[regular_label_size]
        big_size_r = SessionWrapper.size_to_number[big_label_size]
        try_to_save = Database().create_or_update_preferences(user_id, app_mode, main_doctor_id, font_color_r, font_size_r, big_size_r)
        if try_to_save == "okay":
            MessageBoxes.success_message("تم", "تم حفظ الاعدادات")
            self.apply_settings()

    def apply_settings(self):
        user_id = SessionWrapper.user_id
        pref = Database().get_preferences(user_id)
        SessionWrapper.font_color = pref['font_color']
        SessionWrapper.regular_size = pref['regular_size']
        SessionWrapper.big_size = pref['big_size']
        SessionWrapper.app_mode = pref['app_mode']
        SessionWrapper.main_doctor_id = pref['main_doctor_id']
        self.user.update_style()
        regular_style = """
                               QLabel{
                                   color: %s;
                                   font-size: %s;
                                   margin: 0 10px;
                               }
                               """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.main_doctor_label.setStyleSheet(regular_style)
        self.mode_label.setStyleSheet(regular_style)
        self.color_label.setStyleSheet(regular_style)
        self.font_size_label.setStyleSheet(regular_style)
        self.shortcut_1_label.setStyleSheet(regular_style)
        self.shortcut_1_desc.setStyleSheet(regular_style)
        self.shortcut_2_label.setStyleSheet(regular_style)
        self.shortcut_2_desc.setStyleSheet(regular_style)
        self.shortcut_3_label.setStyleSheet(regular_style)
        self.shortcut_3_desc.setStyleSheet(regular_style)
        self.shortcut_4_label.setStyleSheet(regular_style)
        self.shortcut_4_desc.setStyleSheet(regular_style)
        self.shortcut_5_label.setStyleSheet(regular_style)
        self.shortcut_5_desc.setStyleSheet(regular_style)
        self.shortcut_6_label.setStyleSheet(regular_style)
        self.shortcut_6_desc.setStyleSheet(regular_style)
        self.shortcut_7_label.setStyleSheet(regular_style)
        self.shortcut_7_desc.setStyleSheet(regular_style)

        head_style = """
                       QLabel{
                           color: %s;
                           font-size: %s;
                           margin: 0 10px;
                       }
                       """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.big_size])
        self.noteLabel.setStyleSheet(head_style)
        self.shortcuts.setStyleSheet(head_style)

    def mode_changed(self):
        selection = self.sender().currentText()
        if selection == 'طبيب واحد':
            self.main_doctor_select.show()
            self.main_doctor_label.show()
        else:
            self.main_doctor_select.hide()
            self.main_doctor_label.hide()
