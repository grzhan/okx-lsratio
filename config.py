import os

def get_targets():
  raw_text = os.getenv('SCRAPE_TARGETS', 'BTC,ETH,DOGE,SOL')
  return raw_text.split(',')

def get_interval():
  return float(os.getenv('SCRAPE_INTERVAL', 30))

def get_email_sender():
  return os.getenv('EMAIL_SENDER')

def get_email_receiver():
  return os.getenv('EMAIL_RECEIVER')

def get_email_password():
  return os.getenv('EMAIL_PASSWORD')

def get_email_smtp_server():
  return os.getenv('EMAIL_SMTP_SERVER')

def get_email_smtp_port():
  return int(os.getenv('EMAIL_SMTP_PORT', 587))

def get_email_config():
  return {
    'sender': get_email_sender(),
    'receiver': get_email_receiver(),
    'password': get_email_password(),
    'smtp_server': get_email_smtp_server(),
    'smtp_port': get_email_smtp_port(),
  }

def get_lsratio_threshold():
  return float(os.getenv('LSRATIO_THRESHOLD', 20))

def sanitized(text: str):
  return '*' * len(text)

def get_all_configs():
  return [
    ('scrape_interval', get_interval()), 
    ('scrape_targets', ','.join(get_targets())),
    ('email_sender', get_email_sender()),
    ('email_receiver', get_email_receiver()),
    ('email_password', sanitized(get_email_password())),
    ('email_smtp_server', get_email_smtp_server()),
    ('email_smtp_port', get_email_smtp_port()),
    ('lsratio_threshold', get_lsratio_threshold()),
  ]
