from bottle import route, run, template
from config import get_all_configs, get_targets

@route('/')
def index():
  return "okx-lsratio is running"

@route('/config')
def config():
  output = ''
  for key, value in get_all_configs():
    output += f'{key}: {value}<br>'
  return output

@route('/targets')
def targets():
  output = ''
  for target in get_targets():
    output += f'{target}<br>'
  return output


if __name__ == '__main__':
  run(host='0.0.0.0', port=8080)