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
sender_password = "testpass"
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
        except URLError as err:
            return False

    @staticmethod
    def send(subject, message, to="medic.book@yahoo.com"):
        if EmailSender.has_internet():
            receiver = to
            server = smtplib.SMTP(smtp_server, port)
            server.connect(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            # Next, log in to the server
            server.login(sender_email, sender_password)
            # Send the mail
            msg = message  # The /n separates the message from the headers
            server.sendmail(sender_email, receiver, msg)
            server.quit()

    @staticmethod
    def sendemail(from_addr, to_addr_list, subject, message, cc_addr_list=None):
        if EmailSender.has_internet():
            header = 'From: %s' % from_addr
            if type(to_addr_list) is list:
                header += 'To: %s' % ', '.join(to_addr_list)
            else:
                header += 'To: %s' % to_addr_list
            if cc_addr_list:
                if type(cc_addr_list) is list:
                    header += 'Cc: %s' % ', '.join(cc_addr_list)
                else:
                    header += 'Cc: %s' % cc_addr_list
            header += 'Subject: %s' % subject
            message = header + message
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(from_addr, to_addr_list, message)
            server.quit()
            return "Sent"
        else:
            return "Not Internet Connection"

    @staticmethod
    def my_send_email(subject, message):
        if EmailSender.has_internet():
            header = 'From: %s' % sender_email
            header += 'To: %s' % receiver_email
            header += 'Subject: %s' % subject
            message = header + "/n "+message
            server = smtplib.SMTP(smtp_server, port)
            server.connect(smtp_server, port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.encode("utf8"))
            server.quit()
            return "Sent"
        else:
            return "Not Internet Connection"

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


