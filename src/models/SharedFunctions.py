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
from src.models.remoteDatabase import RemoteDatabase


class SharedFunctions:

    @staticmethod
    def logo_image():
        return 'images/icon.png'

    @staticmethod
    def is_leap_year(year):
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        return False

    @staticmethod
    def date_diff_days(from_date, to_date):
        diff_dt = to_date - from_date
        return str(int(diff_dt.days)) + ' Days'

    @staticmethod
    def date_diff_hours(from_date, to_date):
        diff_dt = to_date - from_date
        duration_in_s = diff_dt.total_seconds()
        hours = divmod(duration_in_s, 3600)[0]
        return str(int(hours)) + ' Hours'

    @staticmethod
    def date_diff_minutes(from_date, to_date):
        diff_dt = to_date - from_date
        duration_in_s = diff_dt.total_seconds()
        minutes = divmod(duration_in_s, 60)[0]
        return str(int(minutes)) + ' Minutes'

    @staticmethod
    def date_diff_seconds(from_date, to_date):
        diff_dt = to_date - from_date
        return str(int(diff_dt.total_seconds())) + ' Seconds'

    @staticmethod
    def split_the_name(name):
        parts = name.split(" ")
        second_name = ""
        if len(parts) > 1:
            second_name = parts[1]
        return parts[0], second_name

    @staticmethod
    def date_diff(from_date, to_date):
        end_year = int(to_date.year)
        is_last_year_leap = SharedFunctions.is_leap_year(end_year)
        if is_last_year_leap:
            year_days = 366
            months_limits = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        else:
            year_days = 365
            months_limits = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        diff_dt = to_date - from_date
        duration_in_s = diff_dt.total_seconds()

        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        years = 0
        months = 0
        only_days = int(days[0])
        if only_days > year_days:
            for y in range(from_date.year, to_date.year):
                if only_days >= year_days:
                    years += 1
                    is_leap = SharedFunctions.is_leap_year(y)
                    if is_leap:
                        only_days -= 366
                    else:
                        only_days -= 365
        elif only_days == year_days:
            years = 1
            only_days = 0

        if only_days > months_limits[to_date.month]:
            for m in range(from_date.month, 13):
                if only_days >= months_limits[m]:
                    months += 1
                    only_days -= months_limits[m]
        elif only_days == months_limits[to_date.month]:
            months = 1
            only_days = 0

        if only_days > months_limits[to_date.month]:
            for m2 in range(1, to_date.month+1):
                if only_days >= months_limits[m2]:
                    months += 1
                    only_days -= months_limits[m2]

        if months == 12:
            months = 0
            years += 1
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes

        diff_hours = int(hours[0])
        diff_minutes = int(minutes[0])

        return {'Years': years, 'Months': months, 'Days': only_days, 'Hours': diff_hours, 'Minutes': diff_minutes}

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
    def format_categories(categories):
        formatted_by_id = {}
        formatted_by_name = {}
        for cat in categories:
            formatted_by_id[cat['id']] = {'id': cat['id'], 'name': cat['cat_name'], 'desc': cat['desc']}
            formatted_by_name[cat['cat_name']] = {'id': cat['id'], 'name': cat['cat_name'], 'desc': cat['desc']}
        return formatted_by_id, formatted_by_name

    @staticmethod
    def make_tags_text(tags):
        txt = ''
        for tag in tags:
            txt += ", "+tag['tag_name'].strip()
        return txt[1:]

    @staticmethod
    def delete_cat(cat_id):
        docs = Database().get_docs_ids_for_category(cat_id)
        for opt in docs:
            doc_id = opt['id']
            Database().delete_doc(doc_id)
        Database().delete_cat(cat_id)

    @staticmethod
    def get_desktop_path():
        if SharedFunctions.isWindows():
            desk = os.path.join(os.environ["HOMEPATH"], "Desktop")
            if desk[:2] != 'C:' and desk[:2] != 'c:':
                desk = 'C:'+desk
            return desk
        else:
            return os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

    @staticmethod
    def import_cats(local_cats, remote_cats, user_id):
        current_dat = SharedFunctions.get_current_date_str()
        local_cats_by_name = {}
        for l_cat in local_cats:
            cat_name = l_cat['cat_name']
            local_cats_by_name[cat_name] = l_cat

        for r_cat in remote_cats:
            cat_name = r_cat['cat_name']
            if cat_name not in local_cats_by_name:
                desc = r_cat['desc']
                Database().insert_cat(cat_name, desc, user_id, current_dat)

    @staticmethod
    def import_all_together(local_cats, remote_cats, user_id, db_path):
        current_dat = SharedFunctions.get_current_date_str()
        local_cats_by_name = {}
        for l_cat in local_cats:
            cat_name = l_cat['cat_name']
            local_cats_by_name[cat_name] = l_cat
        db = RemoteDatabase(db_path)
        remote_tags = db.get_all_tags()
        for r_cat in remote_cats:
            cat_name = r_cat['cat_name']
            remote_docs = db.get_docs_for_category(cat_name)
            if cat_name not in local_cats_by_name:
                desc = r_cat['desc']
                cat_id = Database().insert_cat(cat_name, desc, user_id, current_dat)
                SharedFunctions.import_docs_for_all(cat_id, [], remote_docs, remote_tags)
            else:
                cat_id = local_cats_by_name[cat_name]['id']
                local_docs = Database().get_detailed_docs_for_category(cat_id)
                SharedFunctions.import_docs_for_all(cat_id, local_docs, remote_docs, remote_tags)

    @staticmethod
    def merge_import_docs(local_docs, remote_docs, local_tags, remote_tags):
        local_tags_by_doc_id = {}
        for l_tag in local_tags:
            doc_id = l_tag['doc_id']
            local_tags_by_doc_id[doc_id] = []
        remote_tags_by_doc_id = {}
        for r_tag in remote_tags:
            doc_id = r_tag['doc_id']
            remote_tags_by_doc_id[doc_id] = []
        for l_tag in local_tags:
            doc_id = l_tag['doc_id']
            local_tags_by_doc_id[doc_id].append(l_tag)
        for r_tag in remote_tags:
            doc_id = r_tag['doc_id']
            remote_tags_by_doc_id[doc_id].append(r_tag)
        local_docs_by_name = {}
        for l_doc in local_docs:
            name = l_doc['doc_name']
            local_docs_by_name[name] = l_doc
        for r_doc in remote_docs:
            name = r_doc['doc_name']
            remote_doc_id = r_doc['id']
            doc_remote_tags = []
            if remote_doc_id in remote_tags_by_doc_id:
                doc_remote_tags = remote_tags_by_doc_id[remote_doc_id]
            if name in local_docs_by_name:
                local_doc_id = local_docs_by_name[name]['id']
                doc_local_tags = []
                if local_doc_id in local_tags_by_doc_id:
                    doc_local_tags = local_tags_by_doc_id[local_doc_id]
                doc_details = local_docs_by_name[name]['details']+"   "+r_doc['details']
                Database().update_doc_for_import(local_doc_id, doc_details)
                doc_tags = SharedFunctions.decompile_tags(doc_remote_tags, doc_local_tags)
                Database().overwrite_tags(doc_tags, local_doc_id)
            else:
                local_doc_id = Database().insert_doc(r_doc['category_id'], name.strip(), r_doc['details'], "Normal")
                doc_tags = SharedFunctions.decompile_tags(doc_remote_tags)
                Database().insert_tags(doc_tags, local_doc_id)
        return 'Okay'

    @staticmethod
    def import_docs_for_all(cat_id, local_docs, remote_docs, remote_tags):
        remote_tags_by_doc_id = {}
        for r_tag in remote_tags:
            doc_id = r_tag['doc_id']
            remote_tags_by_doc_id[doc_id] = []
        for r_tag in remote_tags:
            doc_id = r_tag['doc_id']
            remote_tags_by_doc_id[doc_id].append(r_tag)
        local_docs_by_name = {}
        for l_doc in local_docs:
            name = l_doc['doc_name']
            local_docs_by_name[name] = l_doc
        for r_doc in remote_docs:
            name = r_doc['doc_name']
            remote_doc_id = r_doc['id']
            doc_remote_tags = []
            if remote_doc_id in remote_tags_by_doc_id:
                doc_remote_tags = remote_tags_by_doc_id[remote_doc_id]
            if name not in local_docs_by_name:
                local_doc_id = Database().insert_doc(cat_id, name.strip(), r_doc['details'], "Normal")
                doc_tags = SharedFunctions.decompile_tags(doc_remote_tags)
                Database().insert_tags(doc_tags, local_doc_id)
        return 'Okay'

    @staticmethod
    def skip_import_docs(local_docs, remote_docs, local_tags, remote_tags):
        local_tags_by_doc_id = {}
        for l_tag in local_tags:
            doc_id = l_tag['doc_id']
            local_tags_by_doc_id[doc_id] = []
        remote_tags_by_doc_id = {}
        for r_tag in remote_tags:
            doc_id = r_tag['doc_id']
            remote_tags_by_doc_id[doc_id] = []
        for l_tag in local_tags:
            doc_id = l_tag['doc_id']
            local_tags_by_doc_id[doc_id].append(l_tag)
        for r_tag in remote_tags:
            doc_id = r_tag['doc_id']
            remote_tags_by_doc_id[doc_id].append(r_tag)
        local_docs_by_name = {}
        for l_doc in local_docs:
            name = l_doc['doc_name']
            local_docs_by_name[name] = l_doc
        for r_doc in remote_docs:
            name = r_doc['doc_name']
            remote_doc_id = r_doc['id']
            doc_remote_tags = []
            if remote_doc_id in remote_tags_by_doc_id:
                doc_remote_tags = remote_tags_by_doc_id[remote_doc_id]
            if name not in local_docs_by_name:
                local_doc_id = Database().insert_doc(r_doc['category_id'], name.strip(), r_doc['details'], "Normal")
                doc_tags = SharedFunctions.decompile_tags(doc_remote_tags)
                Database().insert_tags(doc_tags, local_doc_id)
        return 'Okay'

    @staticmethod
    def decompile_tags(tags1, tags2 = None):
        tags_string = ''
        for tag in tags1:
            if isinstance(tag['tag_name'], str):
                tags_string += ', '+tag['tag_name']
        if tags2 is not None:
            for tag in tags2:
                if isinstance(tag['tag_name'], str):
                    tags_string += ', ' + tag['tag_name']
        return tags_string


if __name__ == '__main__':
    first_date_time = '1984-06-19 10:30:00'
    second_date_time = '2019-04-29 19:40:00'
    print(first_date_time)
    print(second_date_time)
    first_date_time_object = datetime.strptime(first_date_time, "%Y-%m-%d %H:%M:%S")
    second_date_time_object = datetime.strptime(second_date_time, "%Y-%m-%d %H:%M:%S")
    other_diff = SharedFunctions.date_diff(first_date_time_object, second_date_time_object)
    print(other_diff)
