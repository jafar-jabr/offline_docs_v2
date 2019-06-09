"""
settings table:

field1 is_trial bool
field2 trial_start_time nullable
field3 paid_start_time nullable
field4 rows_limit int
field5 pc_id text
field6 default_lng
field7 code_origin
field8 code
"""
from src.models.AppDimensions import AppDimension


class SessionWrapper:
    user_id = None
    user_name = None
    clinic_id = None
    user_email = None
    user_password = None
    user_phone = None
    user_job = None
    user_since = None
    user_role_number = None
    user_role_name = None
    all_the_roles = {1: "مالك التطبيق", 2: "مدير", 3: "مستخدم"}
    all_the_roles_ids = {"مالك التطبيق": 1, "مدير": 2, "مستخدم": 3}
    all_the_jobs = {1: "طبيب", 2: "صيدلاني", 3: "ممرض", 4: "اداري", 5: "مساعد"}
    all_the_jobs_ids = {"طبيب": 1, "صيدلاني": 2, "ممرض": 3, "اداري": 4, "مساعد": 5}
    documents_types = ["Normal", "Image", "Confidential"]
    screen_width = 0
    screen_height = 0
    font_color = "#000"
    regular_size = 18
    big_size = 21
    app_mode = 0  #0 : multibale, 1: single
    main_doctor_id = 0
    color_to_code = {"الابيض": "#ffffff", "الاسود": "#000000", "الاحمر": "#ff0000", "الازرق": "#0000FF"}
    size_to_number = {"16px": 16, "18px": 18, "20px": 20, "21px": 21, "22px": 22, "23px": 23, "24px": 24}
    code_to_color = {"#ffffff": "الابيض", "#fff": "الابيض", "#000000": "الاسود", "#ff0000": "الاحمر", "#0000FF": "الازرق"}
    number_to_size = {16: "16px", 18: "18px", 20: "20px", 21: "21px", 22: "22px", 23: "23px", 24: "24px"}
    screen_dim = ''
    minimum_width = 669

    search_wrapper = {"doctor": 0, "status": 0, "date": 0, "free_search": 0}

    @staticmethod
    def set_user_id(user_id):
        SessionWrapper.user_id = user_id

    @staticmethod
    def get_user_id():
        return SessionWrapper.user_id

    @staticmethod
    def get_dimension(dimension):
        w = SessionWrapper.screen_width
        h = SessionWrapper.screen_height
        return AppDimension(w, h).get_dim(dimension)
