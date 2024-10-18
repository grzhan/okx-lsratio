from bottle import route, run, template, abort
from config import get_all_configs, get_targets
from state import GlobalState
from api import get_margin_loan_ratio
import threading
from monitor import schedule

@route('/')
def index():
  return "okx-lsratio is running"

@route('/config')
def config():
  """
  显示所有配置
  """
  output = ''
  for key, value in get_all_configs():
    output += f'{key}: {value}<br>'
  return output

@route('/targets')
def targets():
  """
  显示所有目标加密货币
  """
  output = ''
  for target in get_targets():
    output += f'{target}<br>'
  return output

@route('/subscribe/<target>')
def subscribe(target):
  """
  订阅目标加密货币
  """
  targets = get_targets()
  if target not in targets:
     abort(404, f'error: target {target} not found')
  state_manager = GlobalState()
  state_manager.subscribe(target)
  return 'ok'

@route('/unsubscribe/<target>')
def unsubscribe(target):
  """
  取消订阅目标加密货币
  """
  state_manager = GlobalState()
  subscriptions = state_manager.get_subscriptions()
  if target not in subscriptions:
     abort(404, f'error: target {target} not found')
  state_manager.unsubscribe(target)
  return 'ok'

@route('/subscriptions')
def subscriptions():
  """
  显示所有订阅的加密货币
  """
  state_manager = GlobalState()
  return state_manager.get_subscriptions()

@route('/daily/report')
def daily_report():
  """
  显示加密货币的当天多空比
  """
  targets = get_targets()
  output = ''
  for target in targets:
    result = get_margin_loan_ratio(target, '1D')
    ratio_str = ''
    if len(result['data']) > 0:
      ratio_str = ', '.join([item[1] for item in result['data']])
    else:
      ratio_str = str(result)
    output += f'{target}: {ratio_str}<br>'
  return output

@route('/latest/report')
def latest_report():
  """
  显示加密货币的最新多空比
  """
  targets = get_targets()
  output = ''
  for target in targets:
    result = get_margin_loan_ratio(target, '5m')
    ratio_str = ''
    if len(result['data']) > 0:
      ratio_str = ', '.join([item[1] for item in result['data']])
    else:
      ratio_str = str(result)
    output += f'{target}: {ratio_str}<br>'
  return output


@route('/alerted/clear')
def clear_alerted():
  """
  清除加密货币的告警记录状态
  """
  state = GlobalState()
  state.clear_alert_record()
  return 'ok'


if __name__ == '__main__':
  thread = threading.Thread(target=schedule)
  thread.start()
  run(host='0.0.0.0', port=8080)
  thread.join()