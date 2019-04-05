from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog, QFileDialog
from PyQt5.QtCore import Qt
from src.Elements.ClickableIcon import ClickableIcon
from src.Elements.ClickableLabel import ClickableLabel
from src.Elements.CustomLabel import RegularLabel
from src.Elements.MaybeLongLabel import MaybeLongLabel
from src.Elements.MessageBoxes import MessageBoxes
from src.dataTables.visitsDataTable import VisitsDataTable
from src.modals.addAppointmentModal import AddAppointmentModal
from src.modals.editPatientModal import EditPatientModal
from src.modals.editVisitModal import EditVisitModal
from src.modals.patientPrintModal import PatientPrintModal
from src.modals.prescriptionPrintModal import PrescriptionPrintModal
from src.models.DatabaseModel import Database
from src.models.PatientReport import PatientReport
from src.models.PrescriptionReport import PrescriptionReport
from src.models.SessionWrapper import SessionWrapper
from src.models.SharedFunctions import SharedFunctions
from src.models.UserBlock import UserBlock
from src.models.Validator import Validator


class PatientDetails(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.parent = parent
        self.visit_id = kwargs["visit_id"]
        details = Database().get_patient_and_visit(self.visit_id)
        self.patient_id = details["id"]
        self.patient_name = details["patient_name"]
        self.patient_details_layout = QVBoxLayout()
        self.patient_details_layout.setSpacing(15)
        self.patient_details_layout.setContentsMargins(0, 0, 0, 20)  # (left, top, right, bottom)
        self.initUI(details)

    def initUI(self, details):
        UserBlock(self)
        clinic_info = QVBoxLayout()
        clinic_info.setContentsMargins(0, 30, 40, 0) # (left, top, right, bottom)

        patient_data_header = QHBoxLayout()
        patient_data_header.setAlignment(Qt.AlignLeft)
        patientDataLabel = RegularLabel('بيانات المراجع : ')

        patient_edit_icon_label = ClickableIcon(35, 35, 'resources/assets/images/edit-icon.png', 'تحديث بيانات المراجع')
        patient_edit_icon_label.clicked.connect(self.update_patient)

        patient_print_label = ClickableIcon(35, 35, 'resources/assets/images/print.png', 'طباعة تقرير المراجع')
        patient_print_label.clicked.connect(self.patient_report)

        patient_data_header.addWidget(patientDataLabel)
        patient_data_header.addWidget(patient_edit_icon_label)
        patient_data_header.addWidget(patient_print_label)

        patient_first_line = QHBoxLayout()
        patient_first_line.setAlignment(Qt.AlignLeft)

        patient_second_line = QHBoxLayout()
        patient_second_line.setAlignment(Qt.AlignLeft)

        patient_data_section = QVBoxLayout()

        self.patientNameLabel = RegularLabel('   الاسم : '+details["patient_name"])

        age = SharedFunctions.calculate_age(details["birth_date"])
        self.ageLabel = RegularLabel('    العمر : '+age)
        self.tallLabel = RegularLabel('    الطول (سم): '+str(details["tall"]))
        self.wieghtLabel = RegularLabel('    الوزن (كغم): '+str(details["weight"]))

        self.phoneLabel = RegularLabel('   الهاتف : '+str(details["phone"]))

        self.gender = RegularLabel('   الجنس : '+str(details["gender"]))

        self.occupation = RegularLabel('   العمل : '+str(details["occupation"]))

        about_h = QHBoxLayout()
        about_h.setSpacing(0)
        about_h.setAlignment(Qt.AlignLeft)
        aboutLabel1 = RegularLabel('   حول : ')
        self.aboutLabel2 = MaybeLongLabel(details["about"], "حول")
        about_h.addWidget(aboutLabel1)
        about_h.addWidget(self.aboutLabel2)

        patient_data_section.addLayout(patient_data_header)
        clinic_info.addLayout(patient_data_section)

        patient_first_line.addWidget(self.patientNameLabel)
        patient_first_line.addWidget(self.ageLabel)
        patient_first_line.addWidget(self.tallLabel)
        patient_first_line.addWidget(self.wieghtLabel)

        patient_second_line.addWidget(self.phoneLabel)
        patient_second_line.addWidget(self.gender)
        patient_second_line.addWidget(self.occupation)

        clinic_info.addLayout(patient_first_line)
        clinic_info.addLayout(patient_second_line)
        clinic_info.addLayout(about_h)

        visit_info = QHBoxLayout()
        visit_info.setAlignment(Qt.AlignLeft)
        visit_info.setContentsMargins(0, 20, 40, 0)  # (left, top, right, bottom)
        the_visit_details = RegularLabel('    تفاصيل الزيارة (المراجعة) : ')
        print_label = ClickableIcon(35, 35, 'resources/assets/images/print.png', 'طباعة تفاصيل الزيارة (الوصفة مثلاً)')
        print_label.clicked.connect(self.print_prescription)
        edit_icon_label = ClickableIcon(35, 35, 'resources/assets/images/edit-icon.png', 'تعديل بيانات الزيارة')
        edit_icon_label.clicked.connect(self.update_visit)

        add_icon_label = ClickableIcon(35, 35, 'resources/assets/images/add-visit.png', 'اضافة موعد زيارة')
        add_icon_label.clicked.connect(self.add_appointment)

        delete_icon_label = ClickableIcon(35, 35, 'resources/assets/images/delete-icon.png', 'حذف بيانات الزيارة')
        delete_icon_label.clicked.connect(self.delete_visit)

        visit_info.addWidget(the_visit_details)
        visit_info.addWidget(add_icon_label)
        visit_info.addWidget(edit_icon_label)
        visit_info.addWidget(print_label)
        visit_info.addWidget(delete_icon_label)

        visit_section = QVBoxLayout()
        visit_section.setContentsMargins(0, 10, 80, 10)  # (left, top, right, bottom)

        self.doctor_name = RegularLabel("اسم الطبيب : "+details["doctor_name"])

        self.visit_date = RegularLabel("التاريخ : "+details["visit_date"] + "                               الوقت : "+SharedFunctions.readableTime(details["visit_time"])+ "                                   الحالة : "+details["visit_status"])

        visit_s_h = QHBoxLayout()
        visit_s_h.setSpacing(0)
        visit_s_h.setAlignment(Qt.AlignLeft)
        visit_symptoms1 = RegularLabel("الاعراض : ")
        self.visit_symptoms2 = MaybeLongLabel(details["symptoms"], "الاعراض")
        visit_s_h.addWidget(visit_symptoms1)
        visit_s_h.addWidget(self.visit_symptoms2)

        visit_d_h = QHBoxLayout()
        visit_d_h.setSpacing(0)
        visit_d_h.setAlignment(Qt.AlignLeft)
        visit_diagnostics1 = RegularLabel("التشخيص : ")
        self.visit_diagnostics2 = MaybeLongLabel(details["diagnosis"], "التشخيص")
        visit_d_h.addWidget(visit_diagnostics1)
        visit_d_h.addWidget(self.visit_diagnostics2)

        visit_p_h = QHBoxLayout()
        visit_p_h.setSpacing(0)
        visit_p_h.setAlignment(Qt.AlignLeft)
        visit_prescription1 = RegularLabel("الوصفة : ")
        self.visit_prescription2 = MaybeLongLabel(details["prescription"], "الوصفة")
        visit_p_h.addWidget(visit_prescription1)
        visit_p_h.addWidget(self.visit_prescription2)

        visit_r_h = QHBoxLayout()
        visit_r_h.setSpacing(0)
        visit_r_h.setAlignment(Qt.AlignLeft)
        visit_recommendation1 = RegularLabel("التوصيات : ")
        self.visit_recommendation2 = MaybeLongLabel(details["recommendations"], "التوصيات")
        visit_r_h.addWidget(visit_recommendation1)
        visit_r_h.addWidget(self.visit_recommendation2)

        visit_images = RegularLabel("الصور ( نتائج التحاليل , صور الاشعة الطبية, الخ) ان وجدت : ")
        images_box = QHBoxLayout()
        # images_box.setAlignment(Qt.AlignRight)
        images_box.setAlignment(Qt.AlignLeft)
        images_box.setContentsMargins(0, 10, 0, 10)  # (left, top, right, bottom)
        images_box.addWidget(visit_images)
        clinic_id = SessionWrapper.clinic_id
        for img in range(5):
            pixmap = QPixmap(SharedFunctions.get_visit_img(clinic_id, self.visit_id, img))
            pixmap_resized1 = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
            label = ClickableLabel()
            label.setObjectName(str(img))
            label.setPixmap(pixmap_resized1)
            label.clicked.connect(self.img_clicked)
            label.rightClicked.connect(self.img_right_clicked)
            images_box.addWidget(label)

        action_line = QHBoxLayout()
        action_line.setSpacing(20)

        images_box.addSpacing(100)
        images_box.addLayout(action_line)

        visit_section.addWidget(self.doctor_name)
        visit_section.addWidget(self.visit_date)
        visit_section.addLayout(visit_s_h)
        visit_section.addLayout(visit_d_h)
        visit_section.addLayout(visit_p_h)
        visit_section.addLayout(visit_r_h)
        visit_section.addLayout(images_box)

        self.patient_details_layout.addLayout(clinic_info)
        self.patient_details_layout.addLayout(visit_info)
        self.patient_details_layout.addLayout(visit_section)
        self.data_table = VisitsDataTable(self.parent, self.patient_id)
        self.patient_details_layout.addWidget(self.data_table)
        self.setLayout(self.patient_details_layout)

    def go_to_edit(self):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to("edit_patient", visit_id=self.visit_id)

    def get_back(self):
        from src.models.PlayMouth import PlayMouth
        PlayMouth(self.parent).go_to("home")

    def add_appointment(self):
        try_to_add = AddAppointmentModal(self.patient_id, self.patient_name).exec_()
        if try_to_add == QDialog.Accepted:
            self.data_table.refresh_data()

    def delete_visit(self):
        if not SharedFunctions.is_manager():
            MessageBoxes.warning_message("خطأ", "ليس لديك الصلاحية للقيام بذلك")
            return
        if SharedFunctions.is_last_visit(self.patient_id):
            return self.delete_patient_and_visit(self.patient_id, self.visit_id)
        txt = "هل انت متأكد من رغبتك بحذف بيانات هذه الزيارة؟"
        check = MessageBoxes.confirm_message(txt)
        if check:
            Database().delete_patient_visit(self.visit_id)
            self.get_back()

    def delete_patient_and_visit(self, patient_id, visit_id):
        txt = "بما ان هذه هي الزيارة الوحيدة لهذا المراجع فأن حذفها يعني ايضاً حذف بيانات المراجع؟"
        check = MessageBoxes.confirm_message(txt)
        if check:
            Database().delete_patient_visit(visit_id)
            Database().delete_patient(patient_id)
            self.get_back()

    def patient_report(self):
        modal = PatientPrintModal(self)
        exe = modal.exec_()
        if exe == QDialog.Accepted:
            logo = modal.show_logo
            path_to_save = modal.selected_path
            PatientReport(self.patient_id, logo, path_to_save)

    def img_clicked(self):
        options = QFileDialog.Options()
        img_path, _ = QFileDialog.getOpenFileName(None, "اختر الصورة", "",
                                                  "Image Files (*.jpg *.png)", options=options)
        img_number = self.sender().objectName()
        if img_path:
            check, message = Validator().validate_image(img_path)
            if not check:
                MessageBoxes.warning_message("خطأ", message)
                return
            clinic_id = SessionWrapper.clinic_id
            SharedFunctions.copy_visit_img(clinic_id, self.visit_id, img_number, img_path)
            pixmap = QPixmap(img_path)
            pixmap_resized1 = pixmap.scaled(60, 60, Qt.KeepAspectRatio)
            self.sender().setPixmap(pixmap_resized1)

    def img_right_clicked(self):
        img_number = self.sender().objectName()
        clinic_id = SessionWrapper.clinic_id
        img = SharedFunctions.get_visit_img(clinic_id, self.visit_id, img_number)
        img_last = img.split('/')[-1]
        if img_last == 'no_visit_image.png':
            pass
        else:
            SharedFunctions.image_viewer(img)

    def print_prescription(self):
        print_options_m = PrescriptionPrintModal(self)
        print_options_n = print_options_m.exec_()
        if print_options_n == QDialog.Accepted:
            selected = print_options_m.selected
            clinic_id = SessionWrapper.clinic_id
            logo = print_options_m.show_logo
            path_to_save = print_options_m.selected_path
            PrescriptionReport(clinic_id, self.visit_id, selected, logo, path_to_save)

    def update_patient(self):
        edit_p_m = EditPatientModal(self)
        edit_p = edit_p_m.exec_()
        if edit_p == QDialog.Accepted and edit_p_m.status == "Done":
            self.update_patient_section()
        elif edit_p == QDialog.Accepted and edit_p_m.status == "Redirect":
            other_patient_id = edit_p_m.other_patient_id
            last_visit_data = Database().get_patient_last_visit(other_patient_id)
            from src.models.PlayMouth import PlayMouth
            PlayMouth(self.parent).go_to("patient_details", visit_id=last_visit_data['id'])

    def update_visit(self):
        edit_v = EditVisitModal(self, self.visit_id).exec_()
        if edit_v == QDialog.Accepted:
            self.update_visit_section()

    def update_patient_section(self):
        details = Database().get_patient_and_visit(self.visit_id)
        self.patientNameLabel.setText('   الاسم : ' + details["patient_name"])
        age = SharedFunctions.calculate_age(details["birth_date"])
        self.ageLabel.setText('    العمر : ' + age)
        self.tallLabel.setText('    الطول (سم): ' + str(details["tall"]))
        self.wieghtLabel.setText('    الوزن (كغم): ' + str(details["weight"]))
        self.phoneLabel.setText('   الهاتف : ' + details["phone"])
        self.aboutLabel2.setText(details["about"])
        self.gender.setText('   الجنس : '+str(details["gender"]))
        self.occupation.setText('   العمل : '+str(details["occupation"]))

    def update_visit_section(self):
        details = Database().get_patient_and_visit(self.visit_id)
        self.doctor_name.setText("اسم الطبيب : "+details["doctor_name"])
        self.visit_date.setText("التاريخ : "+details["visit_date"] + "                               الوقت : "+SharedFunctions.readableTime(details["visit_time"])+ "                                   الحالة : "+details["visit_status"])
        self.visit_symptoms2.setText(details["symptoms"])
        self.visit_diagnostics2.setText(details["diagnosis"])
        self.visit_prescription2.setText(details["prescription"])
        self.visit_recommendation2.setText(details["recommendations"])
        self.data_table.refresh_data()
