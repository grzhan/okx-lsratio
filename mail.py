import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import get_email_config

def send_email(subject: str, content: str):
    config = get_email_config()
    if not config:
        return
    message = MIMEMultipart()
    message['From'] = config['sender']
    message['To'] = config['receiver']
    message['Subject'] = subject
    message.attach(MIMEText(content, 'html'))
    try:
        server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
        server.login(config['sender'], config['password'])
        server.send_message(message)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')


