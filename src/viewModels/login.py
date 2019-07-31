from src.models.DatabaseModel import Database
from src.models.MyEnc import do_encrypt
from src.models.SessionWrapper import SessionWrapper


class LoginModel:
    @staticmethod
    def handleLogin(email, password, remember_me):
        enc_pass = do_encrypt(password)
        check = Database().new_check_login(email)
        if check and check["password"] == enc_pass:
            SessionWrapper.user_password = enc_pass
            SessionWrapper.user_id = check["id"]
            SessionWrapper.user_email = check["email"]
            SessionWrapper.user_since = check["created_at"]
            SessionWrapper.user_name = check["firstname"]+' '+check["lastname"]
            SessionWrapper.user_phone = check['phone']
            LoginModel.get_preferences(check["id"])
            if remember_me:
                Database().update_remember_me(email, password)
            else:
                Database().update_remember_me()
            return 'Okay', "Done"
        elif check and not check["password"]:
            SessionWrapper.user_id = check["id"]
            return "Okay", "new"
        else:
            return "Error", "Invalid Credential"

    @staticmethod
    def get_preferences(user_id):
        pref = Database().get_preferences(user_id)
        try:
            SessionWrapper.font_color = pref['font_color']
            SessionWrapper.regular_size = pref['regular_size']
            SessionWrapper.big_size = pref['big_size']
            SessionWrapper.current_version = pref['current_version']
            SessionWrapper.release_date = pref['release_date']
        except TypeError:
            pass
