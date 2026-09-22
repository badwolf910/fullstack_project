import smtplib
import os
from email.mime.text import MIMEText


def send_mail(customer, email, continent, comments):
    port = int(os.environ.get('SMTP_PORT', '2525'))
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.mailtrap.io')
    login = os.environ.get('SMTP_LOGIN')
    password = os.environ.get('SMTP_PASSWORD')
    if not login or not password:
        raise RuntimeError('SMTP_LOGIN and SMTP_PASSWORD must be configured')
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>continent: {continent}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'dns22668@gmail.com'
    receiver_email = '78a2b46612-6b1214@inbox.mailtrap.io'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
