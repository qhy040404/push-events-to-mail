import os
import smtplib
from email.mime.text import MIMEText

import pandas as pd


def generate_tb(data: list, columns: list):
    print('Generating DataFrame')
    df = pd.DataFrame(data=data, columns=columns)
    return df.to_html(index=False)


def send_email(data: list, columns: list):
    table = generate_tb(data, columns).replace('text-align: right;', 'text-align: center;')
    mail_user = os.getenv('MAIL_USER')
    mail_pass = os.getenv('MAIL_PASS')
    if mail_pass is None or mail_user is None:
        raise Exception('Set MAIL_USER and MAIL_PASS in secrets')
    mail_host = 'smtp.' + mail_user.split('@')[1]

    message = MIMEText(table, 'html', 'utf-8')
    message['Subject'] = 'Daily GitHub Report'
    message['From'] = mail_user
    message['To'] = mail_user

    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
        smtp_obj.login(mail_user, mail_pass)
        smtp_obj.sendmail(mail_user, mail_user, message.as_string())
        print('Mail sent')
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        print('Mail Error')
        print(e)
