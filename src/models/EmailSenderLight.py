# https://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email
# https://docs.python.org/2/library/email-examples.html#id5
import smtplib
from urllib.error import URLError
from urllib.request import urlopen
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import codecs
import re

sender_email = "jafar.ylood@gmail.com"
sender_password = "M@M0288#7"
receiver_email = "medic.book@yahoo.com"
smtp_server = "smtp.gmail.com"
port = 587


class EmailSender:
    def __init__(self):
        pass

    @staticmethod
    def has_internet():
        try:
            urlopen('http://www.google.com', timeout=1)
            return True
        except URLError:
            return False

    @staticmethod
    def send_html_email(subject, message):
        if EmailSender.has_internet():
            me = sender_email
            you = receiver_email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = me
            msg['To'] = you
            file = codecs.open("./resources/assets/emails/contact_us.html", 'r')
            html_template = file.read()
            html_msg = re.sub(r"\bmessage_body\b", message, html_template)
            body = MIMEText(html_msg, 'html')
            msg.attach(body)
            server = smtplib.SMTP(smtp_server, port)
            server.connect(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(me, you, msg.as_string().encode("utf8"))
            server.quit()
            return "Sent"
        else:
            return "Not Internet Connection"
