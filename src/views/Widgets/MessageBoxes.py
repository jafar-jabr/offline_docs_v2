from PyQt5.QtWidgets import QMessageBox


class MessageBoxes:
    def __init__(self):
        pass

    @staticmethod
    def warning_message(title, body):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(body)
        box.setStandardButtons(QMessageBox.Ok)
        buttonOk = box.button(QMessageBox.Ok)
        buttonOk.setText("Okay")
        box.exec_()

    @staticmethod
    def patient_exist(title, body):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(body)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.Ok)
        buttonGo = box.button(QMessageBox.Yes)
        buttonGo.setText("Show Details")
        buttonOk = box.button(QMessageBox.Ok)
        buttonOk.setText("Okay")
        box.exec_()
        if box.clickedButton() == buttonGo:
            return True
        elif box.clickedButton() == buttonOk:
            return False


    @staticmethod
    def confirm_message(text):
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Confirmation!')
        box.setText(text)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Yes')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('Noا')
        box.exec_()
        if box.clickedButton() == buttonY:
            return True
        elif box.clickedButton() == buttonN:
            return False

    @staticmethod
    def success_message(title, body):
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title)
        box.setText(body)
        box.setStandardButtons(QMessageBox.Ok)
        buttonOk = box.button(QMessageBox.Ok)
        buttonOk.setText("Okay")
        box.exec_()

    @staticmethod
    def relogin_message():
        box = QMessageBox()
        box.setIcon(QMessageBox.Question)
        box.setWindowTitle('Confirmation!')
        box.setText("تم تحديث البيانات سوف يتم تطبيق التغييرات بعد تسجيل الخروج والدخول مرة اخرى")
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = box.button(QMessageBox.Yes)
        buttonY.setText('Okay')
        buttonN = box.button(QMessageBox.No)
        buttonN.setText('تسجيل الخروج الان')
        box.exec_()
        if box.clickedButton() == buttonY:
            return True
        elif box.clickedButton() == buttonN:
            return False

    @staticmethod
    def make_order(body, title="expired"):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(body)
        box.setStandardButtons(QMessageBox.Ok)
        buttonOk = box.button(QMessageBox.Ok)
        buttonOk.setText("طلب الاشتراك السنوي")
        box.exec_()
        if box.clickedButton() == buttonOk:
            return True
        return False

    @staticmethod
    def suggest_order(body, title="expired"):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setWindowTitle(title)
        box.setText(body)
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        buttonOk = box.button(QMessageBox.Ok)
        buttonOk.setText("طلب الاشتراك السنوي")
        buttonNo = box.button(QMessageBox.No)
        buttonNo.setText("لا بأس")
        box.exec_()
        if box.clickedButton() == buttonOk:
            return True
        elif box.clickedButton() == buttonNo:
            return False

    @staticmethod
    def make_subscription(body, title="تجديد"):
        box = QMessageBox()
        box.setIcon(QMessageBox.Information)
        box.setWindowTitle(title)
        box.setText(body)
        box.setStandardButtons(QMessageBox.Ok | QMessageBox.No)
        buttonOk = box.button(QMessageBox.Ok)
        buttonOk.setText("لديك كود التفعيل")
        buttonNo = box.button(QMessageBox.No)
        buttonNo.setText("اطلب الان")
        box.exec_()
        if box.clickedButton() == buttonOk:
            return True
        elif box.clickedButton() == buttonNo:
            return False

