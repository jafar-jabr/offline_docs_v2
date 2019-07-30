from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFrame, QDialog, QPushButton, QLineEdit, QMessageBox
from src.Elements.CustomLabel import RegularLabel
from src.models.SessionWrapper import SessionWrapper
from googleapiclient.discovery import build
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle


import datetime


class MyCalendarForm(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__()
        self.setObjectName("my_calendar_page")
        self.parent = parent
        self.clinic_id = SessionWrapper.clinic_id
        self.pages_count = 6
        self.landing_layout = QHBoxLayout()
        self.landing_layout.setContentsMargins(0, 0, 0, 0) #(left, top, right, bottom)
        self.landing_layout.setSpacing(0)
        self.textbox = QLineEdit()
        self.textbox.move(20, 20)
        self.textbox.resize(200,50)
        self.pc_width = SessionWrapper.get_dimension('main_window_width')
        self.pc_height = SessionWrapper.get_dimension('main_window_height')
        self.initUI()

    def googleInit(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        self.events = events_result.get('items', [])

        self.lista = []
        if not self.events:
            print('No upcoming events found.')
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            # print(start, event['summary'])
            self.lista.append(start + event['summary'])

    def on_click(self):
        self.textbox.setText(str([x for x in self.lista]))

    def initUI(self):
        # lbl = RegularLabel("This will be My Calendar page.. coming soon")
        test = RegularLabel(self.googleInit())
        # self.landing_layout.addWidget(lbl)
        self.landing_layout.addWidget(test)
        self.button = QPushButton("Apasa pentru a vedea daca ai evenimente in urmatoarele 10 zile")
        self.button.move(20, 20)
        self.setLayout(self.landing_layout)
        self.landing_layout.addWidget(self.button)
        self.landing_layout.addWidget(self.textbox)

        self.button.clicked.connect(self.on_click)
        print(self.lista)

