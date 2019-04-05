import socket

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from src.Elements.CustomLabel import RegularLabel, HeadLineLabel, UrlLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.Elements.RegularButton import RegularButton
from src.Elements.RegularTextArea import RegularTextArea
from src.models.DatabaseModel import Database
from src.models.OtherThreadAndWait import HandleLongProcess
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.UserBlock import UserBlock
from src.Elements.filteredCompoBox import FilteredCombo


class ContactForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.order = False
        if "order" in kwargs:
            self.order = True
        self.parent = parent
        self.layout_contact = QVBoxLayout()
        self.layout_contact.setContentsMargins(0, 60, 80, 0)  # (left, top, right, bottom)
        self.setFixedHeight(550)
        self.initUI()

    def initUI(self):
        UserBlock(self)
        contact_info = QVBoxLayout()
        contact_info.setSpacing(20)
        contact_info.setAlignment(Qt.AlignLeft)
        contact_info.setContentsMargins(0, 30, 0, 0) #(left, top, right, bottom)
        internetLabel = HeadLineLabel('اذا كان لديك اتصال بالانترنت يمكنك الكتابة الينا الان')

        subjectH = QHBoxLayout()
        subjectLabel = RegularLabel('الموضوع :')
        if Database().is_trial():
            subject_options = ["اختر", "طلب الاشتراك السنوي", "اقتراح", "طلب", "ابلاغ عن خطأ", "موضوع آخر"]
        else:
            subject_options = ["اختر", "اقتراح", "طلب", "ابلاغ عن خطأ", "موضوع آخر"]
        self.subject_select = FilteredCombo(subject_options)
        self.subject_select.setMinimumWidth(250)
        self.subject_select.setLayoutDirection(Qt.RightToLeft)
        subjectH.addWidget(subjectLabel)
        subjectH.addWidget(self.subject_select)
        subjectH.setAlignment(Qt.AlignLeft)
        subjectH.setContentsMargins(0, 0, 0, 40) #(left, top, right, bottom)
        subjectH.setSpacing(20)

        self.messageQ = QWidget()
        messageV = QVBoxLayout()
        messageLabel = RegularLabel('الرسالة :')
        messageV.addWidget(messageLabel)
        messageH = QHBoxLayout()
        messageH.setContentsMargins(0, 0, 50, 0)  # (left, top, right, bottom)
        # self.messageBody = RegularTextArea()

        # messageH.addWidget(self.messageBody)
        messageH.setAlignment(Qt.AlignLeft)
        self.messageBody = RegularTextArea(210, int(self.pc_width*0.3))
        messageH.addWidget(self.messageBody)
        messageV.addLayout(messageH)
        self.messageQ.setLayout(messageV)
        # self.messageQ.setFixedWidth(self.pc_width*0.4)
        btnLine = QHBoxLayout()
        btnLine.setContentsMargins(int(self.pc_width*0.3), 0, 0, 0) #(left, top, right, bottom)
        sendBtn = RegularButton('ارسال')
        sendBtn.clicked.connect(self.do_send_email)
        sendBtn.setMaximumWidth(100)
        btnLine.addWidget(sendBtn)
        alternativeLabel = UrlLabel()
        alternativeLabel.setLayoutDirection(Qt.RightToLeft)
        label_url_text = '<a href="https://www.facebook.com/MedicBookApp/" style="color: %s">كما يمكنك التواصل معنا عبر صفحتنا على الفيسبوك</a>' %SessionWrapper.font_color
        alternativeLabel.setText(label_url_text)
        alternativeLabel.setOpenExternalLinks(True)
        self.layout_contact.addWidget(internetLabel)
        contact_info.addLayout(subjectH)
        contact_info.addWidget(self.messageQ)
        contact_info.addLayout(btnLine)
        self.layout_contact.addLayout(contact_info)
        self.layout_contact.addWidget(alternativeLabel)
        self.layout_contact.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout_contact)
        if self.order:
            self.subject_select.setCurrentText("طلب الاشتراك السنوي")
            self.messageBody.setFocusPolicy(Qt.StrongFocus)
            self.messageBody.focusWidget()

    def do_send_email(self):
        # message = self.messageBody.toPlainText()
        # subject = self.subject_select.currentText()
        # if subject == "اختر":
        #     MessageBoxes.warning_message("خطأ", "الموضوع مطلوب")
        #     return
        # if len(message.strip()) < 4:
        #     MessageBoxes.warning_message("خطأ", "الرسالة قصيرة جداً")
        #     return
        # sender_email = SessionWrapper.user_email
        # sender_name = SessionWrapper.user_name
        # sender_phone = SessionWrapper.user_phone
        # message_body = 'the client: %s, /n with email: %s, /n and phone number: %s, /n Said: %s' % (
        # sender_name, str(sender_email), sender_phone, message)
        # subject = self.subject_select.currentText()
        # if subject == "طلب النسخة الكاملة من البرنامج":
        #     idd = SharedFunctions.prepare_order()
        #     message_body += '     ' + idd
        # send = EmailSender.send_html_email(subject, message_body)
        # if send == "Sent":
        #     self.messageBody.clear()
        #     self.subject_select.setCurrentIndex(0)
        #     MessageBoxes.success_message("تم الارسال", "تم استلام رسالتك وسوف يتم الاجابة عليها باسرع وقت")
        # else:
        #     MessageBoxes.warning_message("خطأ", "لم يتم الارسال, على الاغالب اتصالك بالانترنت ليس بالسرعة المطلوبة")

        try:
            message = self.messageBody.toPlainText()
            subject = self.subject_select.currentText()
            if subject == "اختر":
                MessageBoxes.warning_message("خطأ", "الموضوع مطلوب")
                return
            if len(message.strip()) < 4:
                MessageBoxes.warning_message("خطأ", "الرسالة قصيرة جداً")
                return
            sender_email = SessionWrapper.user_email
            sender_name = SessionWrapper.user_name
            sender_phone = SessionWrapper.user_phone
            message_body = 'the client: %s, /n with email: %s, /n and phone number: %s, /n Said: %s' % (sender_name, str(sender_email), sender_phone, message)
            subject = self.subject_select.currentText()
            if subject == "طلب الاشتراك السنوي":
                idd = SharedFunctions.prepare_order()
                message_body += '     '+idd
            send = HandleLongProcess().do_sending(subject, message_body)
            if send == "Sent":
                self.messageBody.clear()
                self.subject_select.setCurrentIndex(0)
                MessageBoxes.success_message("تم الارسال", "تم استلام رسالتك وسوف يتم الاجابة عليها باسرع وقت")
            else:
                MessageBoxes.warning_message("خطأ", "لم يتم الارسال, على الاغالب اتصالك بالانترنت ليس بالسرعة المطلوبة")
        except socket.timeout:
            MessageBoxes.warning_message("خطأ", "اتصالك بالانترنت ضعيف جداً, لا يمكن ارسال الرسالة الان")
        except:
            MessageBoxes.warning_message("خطأ", "لا يمكن الارسال حالياً, يرجى اعادة المحاولة بعد ساعتين من الان اذا لم تحل المشكلة يرجى التواصل معنا عبر صفحتنا على فيس بوك")
