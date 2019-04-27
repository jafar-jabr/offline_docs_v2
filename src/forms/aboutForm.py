from datetime import datetime, timedelta
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog
from PyQt5.QtCore import Qt
from src.Elements.ClickableLabel import ClickableLabel
from src.Elements.CustomLabel import RegularLabel, HeadLineLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.models.DatabaseModel import Database
from src.models.MyEnc import do_decrypt
from src.models.SessionWrapper import SessionWrapper


class About(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.parent = parent
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.about_layout = QVBoxLayout()
        self.about_layout.setSpacing(20)
        self.initUI()

    def initUI(self):
        about_info = QVBoxLayout()
        about_info.setContentsMargins(0, 60, 60, 0) #(left, top, right, bottom)
        about_first1Label = HeadLineLabel('التطبيق يهدف الى الارتقاء بالخدمات الصحية')
        about_first2Label = HeadLineLabel('من خلال بناء قاعدة بيانات لحفظ وادارة بيانات المراجعين والتاريخ المرضي')
        about_first3Label = HeadLineLabel('للمرضى سواء في العيادات الخاصة للأطباء او  المؤسسات الصحية العامة.')

        emptyLabel1 = RegularLabel()
        emptyLabel2 = RegularLabel()

        second1Label = HeadLineLabel('فريق المطورين قريبون منكم للاستماع الى اسألتكم , اقتراحاتكم وطلباتكم ٢٤\٧')
        second2Label = HeadLineLabel('يتم التحديث بشكل دوري وفي اي وقت عند الحاجة.')

        third1Label = RegularLabel('الاصدار : ١.٠.١')
        third2Label = RegularLabel('تاريخ الاصدار : ١\١\٢٠١٩')

        about_info.addWidget(about_first1Label)
        about_info.addWidget(about_first2Label)
        about_info.addWidget(about_first3Label)

        about_info.addWidget(emptyLabel1)

        about_info.addWidget(second1Label)
        about_info.addWidget(second2Label)

        about_info.addWidget(emptyLabel2)

        about_info.addWidget(third1Label)
        about_info.addWidget(third2Label)

        note_info = QVBoxLayout()
        self.third2note = RegularLabel('')

        self.price_note = RegularLabel()

        app_settings = Database().read_app_settings()
        is_trial = app_settings['field1']
        trial_start_time = app_settings['field2']
        paid_start_time = app_settings['field3']
        if int(is_trial) == 1:
            trial_date = do_decrypt(trial_start_time)
            self.third1note = RegularLabel('انت تستخدم النسخة التجريبية من التطبيق منذ ' + trial_date)
            self.third2note = ClickableLabel('اطلب الاشتراك السنوي ')
            self.third2note.clicked.connect(self.make_order)
            self.price_note = RegularLabel('سعر الاشتراك السنوي ٢٩٩$ (تستطيع الدفع باي طريقة)')
        else:
            appointment_date = do_decrypt(paid_start_time)
            paid_date = datetime.strptime(appointment_date, "%Y-%m-%d")
            now_date_string = datetime.now().strftime('%Y-%m-%d')
            now_date_date = datetime.now().strptime(now_date_string, '%Y-%m-%d')
            paid_due = paid_date + timedelta(365)
            paid_date_str = paid_due.strftime('%Y-%m-%d')
            self.third1note = RegularLabel('اشتراكك السنوي سيبقى فعالاً لغاية ' + paid_date_str)

            delta = paid_due - now_date_date
            diff_ = delta.days
            if diff_ <= 5:
                self.third2note = ClickableLabel('تستطيع تجديد الاشتراك الان ')
                self.third2note.clicked.connect(self.renew)
                self.price_note = RegularLabel('سعر الاشتراك السنوي ٢٩٩$ (تستطيع الدفع باي طريقة)')
        note_info.addWidget(self.third1note)
        note_info.addWidget(self.third2note)
        note_info.addWidget(self.price_note)

        about_info.addLayout(note_info)
        q_about = QWidget()
        q_about.setLayout(about_info)
        q_about.setFixedHeight(700)
        self.about_layout.addWidget(q_about)
        self.about_layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.about_layout)

    def do_update_view(self):
        app_settings = Database().read_app_settings()
        paid_start_time = app_settings['field3']
        appointment_date = do_decrypt(paid_start_time)
        paid_date = datetime.strptime(appointment_date, "%Y-%m-%d")
        paid_due = paid_date + timedelta(365)
        paid_date_str = paid_due.strftime('%Y-%m-%d')
        self.third1note.setText('اشتراكك السنوي سيبقى فعالاً لغاية ' + paid_date_str)
        self.third2note.setText('  ')
        self.third2note.hide()
        self.price_note.hide()

    def renew(self):
        ask = MessageBoxes.make_subscription('تجديد الاشتراك')
        if ask:
            pass
        else:
            from src.models.PlayMouth import PlayMouth
            PlayMouth(self.parent).go_to("contact", order=True)

    def make_order(self):
        ask = MessageBoxes.make_subscription('طلب الاشتراك', 'اشتراك')
        if ask:
            pass
        else:
            from src.models.PlayMouth import PlayMouth
            PlayMouth(self.parent).go_to("contact", order=True)
