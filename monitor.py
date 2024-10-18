import os
import time
from config import get_targets
from datetime import datetime
from state import GlobalState
from api import get_margin_loan_ratio
from mail import send_email
from config import get_lsratio_threshold

def send_daily_report(date: str):
  """对于关心的加密货币调用 OKX API，获取过去 24 小时的多空比，并作为日报发送邮件"""
  output = ''
  targets = get_targets()
  for target in targets:
    result = get_margin_loan_ratio(target, '1D')
    if len(result['data']) > 0:
      ratio_str = ', '.join([item[1] for item in result['data']])
    else:
      ratio_str = str(result)
    output += f'{target}: {ratio_str}<br>'
  send_email(f'【日报】加密货币多空比 - {date}', output)

def check_lsratio_and_alert(target: str):
  """检查订阅已入场的加密货币，调用 OKX API，获取过去 5 分钟的多空比，如果其多空比小于预设阈值，则发送邮件提醒"""
  result = get_margin_loan_ratio(target, '5m')
  threshold = get_lsratio_threshold()
  state = GlobalState()
  if len(result['data']) > 0:
    ratio = float(result['data'][0][1])
    if ratio < threshold:
      send_email(f'【风险】{target} 多空比小于 {threshold}', f'{target} 多空比为 {ratio}，小于阈值 {threshold}，请注意风险')
      state.mark_as_alerted(target)
  else:
    print(f'No lsratio data for {target}')
    print(result)


def schedule():
  interval = float(os.getenv('SCRAPE_INTERVAL', 30))
  record_date = ''
  state = GlobalState()
  while True:
    try:
      current_date = datetime.now().strftime('%Y-%m-%d')
      current_time = datetime.now().strftime('%H')
      if current_time == '01' and current_date != record_date:
        record_date = current_date
        send_daily_report(current_date)
      subscriptions = state.get_subscriptions()
      if len(subscriptions) > 0:
        for target in subscriptions:
          if state.check_if_alerted(target):
            continue
          check_lsratio_and_alert(target)
    except Exception as e:
      print(e)
    time.sleep(interval)