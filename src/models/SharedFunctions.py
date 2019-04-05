import ctypes
import os
import shutil
import sys
import subprocess
import uuid
from datetime import datetime, timedelta
import calendar
import string
import random
from src.Elements.MessageBoxes import MessageBoxes
from src.models.DatabaseModel import Database
from src.models.MyEnc import do_encrypt, do_decrypt
from src.models.SessionWrapper import SessionWrapper


class SharedFunctions:

    @staticmethod
    def logo_image():
        return 'images/icon.png'

    @staticmethod
    def calculate_age(b):
        try:
            b = datetime.strptime(b, "%d-%m-%Y")
        except ValueError:
            b = datetime.strptime(b, "%Y-%m-%d")
        t = datetime.now()
        # b = datetime.strptime('1-07-2018', "%d-%m-%Y")
        # t = datetime.strptime('31-07-2018', "%d-%m-%Y")
        c = ((t.month, t.day) < (b.month, b.day))
        c2 = (t.day < b.day)
        birth_month_days = calendar.monthrange(b.year, b.month)[1]
        age_years = t.year - b.year - c
        age_months = c * 12 + t.month - b.month - c2
        age_days = c2 * birth_month_days + t.day - b.day
        if age_days >= 30:
            age_days = 0
            age_months += 1
        age = ''
        if age_years > 0:
            if age_years == 1:
                age += str(age_years) + ' سنة '
            elif age_years <= 10:
                age += str(age_years) + ' اعوام '
            else:
                age += str(age_years) + ' عام '
        if age_months > 0:
            if age_months == 1:
                age += str(age_months) + ' شهر '
            else:
                age += str(age_months) + ' اشهر '
        if age_days > 0:
            if age_days == 1:
                age += str(age_days) + ' يوم'
            else:
                age += str(age_days) + ' ايام'
        if len(age) == 0:
            age = ' 1 يوم '
        return age

    @staticmethod
    def days_between(d1, d2):
        c2 = (d2.day < d1.day)
        birth_month_days = calendar.monthrange(d1.year, d1.month)[1]
        diff_days = c2 * birth_month_days + d2.day - d1.day
        return diff_days

    @staticmethod
    def some_spaces(num):
        txt = ""
        for n in range(num):
            txt +=" "
        return txt

    @staticmethod
    def format_doctors_list(doctors_list, first=None):
        if first:
            formatted_list = [first]
        else:
            formatted_list = []
        for row in doctors_list:
            for name in row:
                formatted_list.append(name)
        return formatted_list

    @staticmethod
    def format_text(txt, length=0, with_dots=True):
        txt_f = str(txt)
        if len(txt_f) == 0 or txt is None:
            return 'Null'
        if length == 0:
            length = len(txt)
        elif length > 100:
            length = 100
        extra_length = len(txt) - length
        new_length = length
        if extra_length > 0:
            new_string = txt[:length]
            the_index = new_string.rfind(' ')
            if the_index > 0:
                new_length = the_index
            if with_dots:
                new_length += 4
                if the_index:
                    txt = new_string[:the_index] + ' ...  '
                else:
                    txt = new_string + '...  '
            else:
                if the_index:
                    txt = new_string[:the_index]
                else:
                    txt = new_string
        # elif extra_length < 0:
        #     add = length - len(txt)
        #     if add > 0:
        #         for addition in range(0, add):
        #             txt += ' '
        return txt.replace('\n', ' ').replace('\r', '')

    @staticmethod
    def copy_profile_img(user_id, img_path):
        if len(img_path) > 3:
            ext = os.path.splitext(img_path)[1][1:]
            profile_img = "resources/assets/images/profile_images/profile_" + str(user_id)+"."+ext
            if os.path.exists("resources/assets/images/profile_images/profile_" + str(user_id)+".png"):
                os.remove("resources/assets/images/profile_images/profile_" + str(user_id)+".png")
            if os.path.exists("resources/assets/images/profile_images/profile_" + str(user_id)+".jpg"):
                os.remove("resources/assets/images/profile_images/profile_" + str(user_id)+".jpg")
            shutil.copy(img_path, profile_img)

    @staticmethod
    def copy_logo_img(clinic_id, img_path):
        if len(img_path) > 3:
            ext = os.path.splitext(img_path)[1][1:]
            profile_img = "resources/assets/images/logo_images/logo_" + str(clinic_id) + "." + ext
            if os.path.exists("resources/assets/images/logo_images/logo_" + str(clinic_id) + ".png"):
                os.remove("resources/assets/images/logo_images/logo_" + str(clinic_id) + ".png")
            if os.path.exists("resources/assets/images/logo_images/logo_" + str(clinic_id) + ".jpg"):
                os.remove("resources/assets/images/logo_images/logo_" + str(clinic_id) + ".jpg")
            shutil.copy(img_path, profile_img)

    @staticmethod
    def copy_visit_img(clinic_id, visit_id, img_number, img_path):
        if len(img_path) > 3:
            ext = os.path.splitext(img_path)[1][1:]
            profile_img = "resources/assets/images/visit_images/visit_" + str(clinic_id)+'_'+str(visit_id)+'_'+str(img_number) + "." + ext
            if os.path.exists("resources/assets/images/visit_images/visit_" + str(clinic_id)+'_'+str(visit_id)+'_'+str(img_number) +  ".png"):
                os.remove("resources/assets/images/visit_images/visit_" + str(clinic_id)+'_'+str(visit_id)+'_'+str(img_number) +  ".png")
            if os.path.exists("resources/assets/images/visit_images/visit_" + str(clinic_id)+'_'+str(visit_id)+'_'+str(img_number) +  ".jpg"):
                os.remove("resources/assets/images/visit_images/visit_" + str(clinic_id)+'_'+str(visit_id)+'_'+str(img_number) +  ".jpg")
            shutil.copy(img_path, profile_img)

    @staticmethod
    def get_visit_img(clinic_id, visit_id, img_number):
        if os.path.exists("resources/assets/images/visit_images/visit_" + str(clinic_id) + '_' + str(visit_id) + '_' + str(img_number) + ".png"):
            return "resources/assets/images/visit_images/visit_" + str(clinic_id) + '_' + str(visit_id) + '_' + str(img_number) + ".png"
        elif os.path.exists("resources/assets/images/visit_images/visit_" + str(clinic_id) + '_' + str(visit_id) + '_' + str(img_number) + ".jpg"):
            return "resources/assets/images/visit_images/visit_" + str(clinic_id) + '_' + str(visit_id) + '_' + str(img_number) + ".jpg"
        else:
            return 'resources/assets/images/no_visit_image.png'

    @staticmethod
    def get_logo_img(clinic_id):
        if os.path.exists("resources/assets/images/logo_images/logo_" + str(clinic_id) + ".png"):
            return "resources/assets/images/logo_images/logo_" + str(clinic_id) + ".png"
        elif os.path.exists(
                "resources/assets/images/logo_images/logo_" + str(clinic_id) + ".jpg"):
            return "resources/assets/images/logo_images/logo_" + str(clinic_id) + ".jpg"
        else:
            return False

    @staticmethod
    def readableTime(time):
        only_time = time.split(" ")[1]
        time_part = only_time.split(":")
        hours = int(time_part[0])
        minutes = time_part[1]
        sign = "ص"
        if hours > 12:
            hours = str(hours-12)
            sign = "م"
        else:
            hours = str(hours)
            sign = "ص"
        return hours+":"+minutes+" "+sign

    @staticmethod
    def only_time(time):
        return time.split(" ")[1]

    @staticmethod
    def is_manager():
        if SessionWrapper.user_role_number < 3:
            return True
        return False

    @staticmethod
    def get_current_date_str():
        now = datetime.now()
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        if len(month) == 1:
            month = "0"+month
        if len(day) == 1:
            day = "0"+day
        return year + "-" + month + "-" + day

    @staticmethod
    def get_current_day_str():
        now = datetime.now()
        day = str(now.day)
        if len(day) == 1:
            day = "J" + day
        return day

    @staticmethod
    def get_current_month_str():
        now = datetime.now()
        month = str(now.month)
        if len(month) == 1:
            month = "J" + month
        return month

    @staticmethod
    def get_main_doctor():
        main_doctor_id = SessionWrapper.main_doctor_id
        if main_doctor_id:
            doctor = Database().get_user_name_by_id(main_doctor_id)
            if doctor:
                return doctor
        clinic_id = SessionWrapper.clinic_id
        return Database().get_default_doctor(clinic_id)

    @staticmethod
    def image_viewer(file_full_name):
        if SharedFunctions.isWindows():
            SharedFunctions.windows_show_image(file_full_name)
        else:
            opener = {'linux': 'xdg-open', 'win32': 'explorer', 'darwin': 'open'}[sys.platform]
            subprocess.call([opener, file_full_name])

    @staticmethod
    def is_future(date_staring):
        given_date = datetime.strptime(date_staring, "%Y-%m-%d")
        now_date_string = datetime.now().strftime('%Y-%m-%d')
        now_date_date = datetime.now().strptime(now_date_string, '%Y-%m-%d')
        if given_date <= now_date_date:
            return False
        else:
            return True

    @staticmethod
    def is_past(date_staring):
        given_date = datetime.strptime(date_staring, "%Y-%m-%d")
        now_date_string = datetime.now().strftime('%Y-%m-%d')
        now_date_date = datetime.now().strptime(now_date_string, '%Y-%m-%d')
        if given_date >= now_date_date:
            return False
        else:
            return True

    @staticmethod
    def get_word_path():
        try:
            import winreg
        except ImportError:
            import _winreg as winreg

        try:
            handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\winword.exe")
            path = winreg.EnumValue(handle, 0)
            return path[1]
        except FileNotFoundError:
            return False

    @staticmethod
    def windows_show_image(path):
        # subprocess.call(['explorer', path])
        from PIL import Image
        image = Image.open(path)
        image.show()

    @staticmethod
    def isWindows():
        return sys.platform == 'win32'

    @staticmethod
    def maybeLongString(txt, limit=50):
        if type(txt) == str and len(txt) > limit:
            return txt[:limit]+' ...'
        elif type(txt) == str:
            return txt
        return 'None'

    @staticmethod
    def open_word(path_to_file):
        try:
            if SharedFunctions.isWindows():
                path_to_word = SharedFunctions.get_word_path()
                if path_to_word:
                    # p = subprocess.Popen([path_to_word, path_to_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                    p = subprocess.Popen([path_to_word, path_to_file])
                else:
                    MessageBoxes.warning_message("خطأ", "يبدوا ان مايكروسوفت اوفس غير مثبت على الجهاز")
                    return
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, path_to_file])
        except Exception as e:
            MessageBoxes.warning_message("خطأ", path_to_file)
            MessageBoxes.warning_message("خطأ", str(e))
            return

    @staticmethod
    def check_point(sender='first'):
        # field10 if 10 is just installed
        check_result = True
        do_order = False
        app_settings = Database().read_app_settings()
        is_trial = app_settings['field1']
        trial_start_time = app_settings['field2']
        paid_start_time = app_settings['field3']
        rows_limit = app_settings['field4']
        pc_id = app_settings['field5']
        default_lng = app_settings['field6']

        if len(str(pc_id)) < 10 and app_settings['field10'] == 10:
            pc_idd = SharedFunctions.get_pc_id()
            enc_id = do_encrypt(pc_idd)
            Database().update_pc_id(enc_id)
        elif do_decrypt(pc_id) == SharedFunctions.get_pc_id():
                pass
        else:
            MessageBoxes.warning_message('خطأ',  'لم يتم التعرف على النظام يرجى اعادة تنصيب التطبيق ')
            return False, False
        if int(is_trial) == 1:
            if len(str(trial_start_time)) < 5:
                current_date = SharedFunctions.get_current_date_str()
                # current_date = '2019-02-10'
                enc_date = do_encrypt(current_date)
                Database().update_trial_time(enc_date)
                trial_start_time = current_date
            else:
                trial_start_time = do_decrypt(app_settings['field2'])
            trial_date = datetime.strptime(trial_start_time, "%Y-%m-%d")
            now_date_string = datetime.now().strftime('%Y-%m-%d')
            now_date_date = datetime.now().strptime(now_date_string, '%Y-%m-%d')
            trial_due = trial_date + timedelta(30)
            delta = trial_due - now_date_date
            diff_ = delta.days
            if diff_ <= 0:
                disclaimer = """لقد تجازوت الحد المسموح به لاستخدام النسخة المجانية  اذا كنت ترغب في الاستمرار باستخدام التطبيق اطلب الاشتراك السنوي للحصول على سنة (٣٦٥ يوم) اخرى"""
                order = MessageBoxes.make_order(disclaimer, "خطأ")
                if order:
                    do_order = True
                check_result = False
            elif diff_ <= 5:
                order = MessageBoxes.suggest_order("انت على وشك استنفاذ الحد المسموح به لاستخدام النسخة التجريبية", "تحذير")
                if order:
                    do_order = True
        else:
            if len(str(paid_start_time)) < 5:
                current_date = SharedFunctions.get_current_date_str()
                enc_date = do_encrypt(current_date)
                Database().update_paid_time(enc_date)
                paid_start_time = current_date
            else:
                paid_start_time = do_decrypt(app_settings['field3'])
            paid_date = datetime.strptime(paid_start_time, "%Y-%m-%d")
            now_date_string = datetime.now().strftime('%Y-%m-%d')
            now_date_date = datetime.now().strptime(now_date_string, '%Y-%m-%d')
            paid_due = paid_date + timedelta(365)
            delta = paid_due - now_date_date
            diff_ = delta.days
            if diff_ <= 0:
                disclaimer = """لقد تجازوت الحد المسموح به لاستخدام الاشتراك السنوي
            اذا كنت ترغب في الاستمرار باستخدام التطبيق                
            اطلب الاشتراك لسنة اخرى                
                            """
                order = MessageBoxes.make_order(disclaimer, "خطأ")
                if order:
                    do_order = True
                check_result = False
            elif diff_ <= 5 and sender == 'first':
                order = MessageBoxes.suggest_order("انت على وشك استنفاذ الحد المسموح به لاستخدام الاشتراك السنوي",
                                                "تحذير")
                if order:
                    do_order = True
            else:
                code_origin = do_decrypt(app_settings['field7'])
                code = app_settings['field8']
                if code != code_origin:
                    order = MessageBoxes.make_order("كود التسجيل غير صالح",
                                                    "تحذير")
                    if order:
                        do_order = True
                    check_result = False
        return check_result, do_order

    @staticmethod
    def prepare_order():
        pc_id = SharedFunctions.get_pc_id()
        c_1 = pc_id[3]
        c_2 = pc_id[7]
        c_3 = pc_id[4]
        c_4 = pc_id[8]
        chars = string.ascii_uppercase + string.digits
        size = 16
        code = ''.join(random.choice(chars) for _ in range(size))
        f_code = '-'.join(code[i:i+4] for i in range(0, len(code), 4))
        replace1 = f_code[:3] + c_1 + f_code[4:]
        replace2 = replace1[:7] + c_2 + replace1[8:]
        replace3 = replace2[:11] + c_3 + replace2[12:]
        replace4 = replace3[:15] + c_4 + replace3[16:]
        day_string = SharedFunctions.get_current_day_str()
        month_string = SharedFunctions.get_current_month_str()

        replace5 = month_string+replace4[2:]
        replace6 = replace5[:12]+day_string+replace5[14:]
        enc_code = do_encrypt(replace6)
        Database().update_code_origin(enc_code)
        return '        the code is  '+replace6 + '   And the pc_id is '+pc_id

    @staticmethod
    def get_date_from_code(the_code):
        day_1 = the_code[12:14].replace('J', '')
        month_1 = the_code[:2].replace('J', '')
        now = datetime.now()
        year = str(now.year)
        date_ob = datetime.strptime(day_1+'-'+month_1+'-'+year, "%d-%m-%Y")
        if date_ob > now:
            year = str(now.year-1)
            date_ob = datetime.strptime(day_1 + '-' + month_1 + '-' + year, "%d-%m-%Y")
        return date_ob.strftime('%Y-%m-%d')

    @staticmethod
    def is_last_visit(patient_id):
        visits_count = Database().count_patient_visit(patient_id)
        if int(visits_count) == 1:
            return True
        return False

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def get_pc_id():
        id1 = uuid.getnode()
        id2 = uuid.getnode()
        if id1 == id2:
            return str(id1)
        return False

    @staticmethod
    def get_desktop_path():
        if SharedFunctions.isWindows():
            desk = os.path.join(os.environ["HOMEPATH"], "Desktop")
            if desk[:2] != 'C:' and desk[:2] != 'c:':
                desk = 'C:'+desk
            return desk
        else:
            return os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

# if __name__ == '__main__':
#     enc = SharedFunctions.prepare_order()
#     print(enc)
