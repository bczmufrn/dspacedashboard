import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from decouple import config

def send_mail(recipient, template_name, params=[]):
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

    msg = MIMEMultipart()

    try:
        file = open(os.path.join(templates_dir, template_name), 'r')
        message = file.read()
        file.close()

        message = message.format(*params)

        msg['From'] = "repositorio@bczm.ufrn.br"
        msg['To'] = recipient
        msg['Subject'] = "[Não responder] - Repositório Institucional"

        msg.attach(MIMEText(message, 'plain'))

        server_ssl = smtplib.SMTP_SSL(config('SMTP_HOST'), config('SMTP_PORT'))
        server_ssl.login(config('SMTP_LOGIN'), config('SMTP_PASS'))
        server_ssl.sendmail(msg['From'], msg['To'], msg.as_string())
        server_ssl.close()

    except Exception as e:
        print(e)