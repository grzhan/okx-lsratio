import os

def get_targets():
  raw_text = os.getenv('SCRAPE_TARGETS')
  return raw_text.split(',')

def get_interval():
  return float(os.getenv('SCRAPE_INTERVAL', 5))

def get_all_configs():
  return [
    ('scrape_interval', get_interval()), 
    ('scrape_targets', os.getenv('SCRAPE_TARGETS'))
  ]
