import os
import time
from config import get_targets


def run():
  interval = float(os.getenv('SCRAPE_INTERVAL', 5))
  targets = get_targets()
  while True:
    time.sleep(interval)