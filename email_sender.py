import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, sender: str, password: str):
        self.sender = sender
        self.password = password

    def send_email(self, subject: str, body: str, recipients: list[str]) -> None:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, recipients, msg.as_string())
