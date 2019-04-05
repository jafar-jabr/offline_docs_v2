import os

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QLabel
from src.Elements.CustomLabel import MidSizeLabel
from src.models import RoundedImage
from src.models.SessionWrapper import SessionWrapper


class UserBlock:
    def __init__(self, parent):
        user_id = SessionWrapper.user_id
        user_name_d = SessionWrapper.user_name[:11]
        job_d = SessionWrapper.user_job
        since_b = SessionWrapper.user_since
        self.user_name = MidSizeLabel("اسم المستخدم: "+user_name_d, parent)
        self.user_name.setGeometry(QRect(120, parent.y()+30, 300, 45)) #(x, y, width, height)
        self.job_title = MidSizeLabel("العنوان الوظيفي: "+job_d, parent)
        self.job_title.setGeometry(QRect(self.user_name.x(), self.user_name.y()+35, 300, 45))  # (x, y, width, height)
        self.registration_date = MidSizeLabel("تاريخ التسجيل: "+since_b, parent)
        self.registration_date.setGeometry(QRect(self.user_name.x(), self.user_name.y() + 70, 300, 45))  # (x, y, width, height)
        extension = "png"
        file_name = "resources/assets/images/profile_images/profile_"+str(user_id)
        if os.path.isfile(file_name+".jpg"):
            imgpath = file_name+".jpg"
            extension = "jpg"
        elif os.path.isfile(file_name+".png"):
            imgpath = file_name+".png"
        else:
            imgpath = "resources/assets/images/user_image.png"
        pixmap = RoundedImage.maskImage(imgpath, extension)
        self.ilabel = QLabel("r", parent)
        self.ilabel.setPixmap(pixmap)
        self.ilabel.setGeometry(QRect(0, self.user_name.y()-30, 170, 170))  # (x, y, width, height)

    def update_style(self):
        style = """
                       QLabel{
                           color: %s;
                           font-size: %s;
                           margin: 0 10px;
                       }
                       """ % (SessionWrapper.font_color, SessionWrapper.number_to_size[SessionWrapper.regular_size])
        self.job_title.setStyleSheet(style)
        self.user_name.setStyleSheet(style)
        self.registration_date.setStyleSheet(style)

    def update_name(self, name):
        self.user_name.setText("اسم المستخدم: " + name)

    def update_image(self, img):
        extension = img.split('.')[-1]
        pixmap = RoundedImage.maskImage(img, extension)
        self.ilabel.setPixmap(pixmap)
