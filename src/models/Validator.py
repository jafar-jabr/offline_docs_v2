import os
import re
from datetime import datetime
from PyQt5.QtGui import QImage
from src.models.DatabaseModel import Database


class Validator:
    number_pattern = r"(^[0123456789 ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ +]+$)"
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    @staticmethod
    def validate_name(_name):
        _name = _name.replace(" ", "")
        if len(_name) == 0 or len(_name) < 4:
            return False, "The name is too short"
        if Validator.has_numbers(_name):
            return False, "The name can not contain numbers"
        elif 3 <= len(_name) <= 50:
            return True, "Okay"
        return False, "The name is invalid"

    @staticmethod
    def validate_email(_email):
        if not _email:
            return True, "Okay"
        if re.match(Validator.email_pattern, _email):
            if 5 <= len(_email) <= 60:
                return True, "Okay"
        return False, "The email is not valid"

    @staticmethod
    def validate_passwords(_pass_1, _pass_2):
        if len(_pass_1) < 6:
            return False, 'Password can not be less than 6 characters'
        elif _pass_1 != _pass_2:
            return False, 'The password and its confirmation does not match'
        return True, "Okay"

    @staticmethod
    def validate_phone(_phone, optional=False):
        _phone = _phone.replace(" ", "")
        if optional and len(_phone) == 0:
            return True, "Okay"
        if re.match(Validator.number_pattern, _phone):
            if 10 <= len(_phone) <= 14:
                return True, "Okay"
        return False, "رقم الهاتف غير صالح"

    @staticmethod
    def validate_occupation(_occupation):
        _occupation = _occupation.replace(" ", "")
        if len(_occupation) == 0:
            return True, "Okay"
        if Validator.has_numbers(_occupation):
            return False, "العمل لا يمكن ان يحتوي على ارقام"
        if 3 <= len(_occupation):
                return True, "Okay"
        return False, "العمل غير صالح"

    @staticmethod
    def validate_image(_img_path):
        try:
            imgtype = os.path.splitext(_img_path)[-1][1:]
            imgdata = open(_img_path, 'rb').read()
            image = QImage.fromData(imgdata, imgtype)
            image.convertToFormat(QImage.Format_ARGB32)
            return True, "Okay"
        except IOError:
            return False, "ملف الصورة غير صالح"
        except:
            return False, "ملف الصورة غير صالح"

    @staticmethod
    def validate_option(_option, msg):
        if _option == "اختر":
            return False, msg
        return True, "okay"

    @staticmethod
    def validate_doctor_name(_doctor_name):
        if _doctor_name == "اختر":
            return False, "اسم الطبيب مطلوب"
        else:
            doctor_id = Database().get_doctor_id(_doctor_name)
            if doctor_id == 0:
                return False, "اسم الطبيب غير موجود"
        return True, "okay"

    @staticmethod
    def validate_specialization(_specialization, _job):
        if _job == "طبيب":
            if len(_specialization) < 3:
                return False, "الاختصاص قصير جداً"
        return True, "Okay"

    @staticmethod
    def validate_height(_h):
        if len(_h.strip()) > 0:
            if int(_h) > 251:
                return False, "الطول اكبر من الحد الاعلى الطبيعي, اطول رجل في العالم يبلغ طوله ٢٥١ سم !"
            elif 0 < int(_h) < 10:
                return False, " الطول اقل من الحد الادنى الطبيعي !"
        return True, "okay"

    @staticmethod
    def validate_weight(_w):
        if len(_w.strip()) > 0:
            if int(_w) > 610:
                return False, " الوزن اكبر من الحد الاعلى الممكن للانسان !"
            elif 0 < int(_w) < 1:
                return False, " الوزن اقل من الحد الادنى الممكن للانسان !"
        return True, "okay"

    @staticmethod
    def validate_date(date_staring, name="التاريخ", **kwargs):
        try:
            given_date = datetime.strptime(date_staring, "%Y-%m-%d")
            now_date_string = datetime.now().strftime('%Y-%m-%d')
            now_date_date = datetime.now().strptime(now_date_string, '%Y-%m-%d')
            if "future" in kwargs and kwargs["future"]:
                if given_date < now_date_date:
                    return False, name+" لا يمكن ان يكون في الماضي !"
            if "past" in kwargs and kwargs["past"]:
                if given_date > now_date_date:
                    return False, name+" لا يمكن ان يكون في المستقبل !"
            return True, "Okay"
        except ValueError:
            return False, name+" غير صالح !"
        except:
            return False, name+" غير صالح !"

    @staticmethod
    def validate_clinic_specialization(_specialization):
        _specialization = _specialization.replace(" ", "")
        if len(_specialization) == 0:
            return False, "الاختصاص مطلوب"
        if Validator.has_numbers(_specialization):
            return False, "الاختصاص لا يمكن ان يحتوي على ارقام"
        else:
            return True, "Okay"

    @staticmethod
    def validate_address(_address):
        _address = _address.replace(" ", "")
        if len(_address) == 0:
            return False, "العنوان مطلوب"
        if len(_address) < 6:
            return False, "العنوان قصير جداً"
        else:
            return True, "Okay"

    @staticmethod
    def has_numbers(input_string):
        return any(char.isdigit() for char in input_string)

    @staticmethod
    def validate_from_to_date(date_from, date_to):
        from_date = datetime.strptime(date_from, "%Y-%m-%d")
        to_date = datetime.strptime(date_to, "%Y-%m-%d")
        if from_date > to_date:
            return False, 'تاريخ نهاية التقرير لا يمكن ان يكون قبل تاريخ بدايته'
        elif from_date == to_date:
            return False, 'تاريخ نهاية التقرير يجب ان يكون بعد تاريخ بدايته'
        return True, 'okay'
