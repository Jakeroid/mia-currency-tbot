from flask import Flask, url_for, render_template, request
import json
import urllib.request
import requests
import sys
from config import get_config

# prepare app object
app = Flask(__name__, static_folder='static', static_url_path='')

# main variables
config = get_config()
telegram_api_url = "https://api.telegram.org/bot%s/" % config.get('telegram_bot_api_token')
hook_url_path = '/hook/%s' % config.get('telegram_bot_api_token')
hook_absolute_url = 'https://mia-currency-tbot.jakeroid.com%s' % hook_url_path
log_data = [];

# set web hook function
def set_web_hook():
    result_url = '%ssetWebHook?url=%s' % (telegram_api_url, hook_absolute_url)
    resource = urllib.request.urlopen(result_url)
    content =  resource.read().decode('utf-8')
    answer = json.loads(content)
    flag = answer.get('ok')
    return flag

# function for parse currency
def parse_urd_current():
    result_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    resource = urllib.request.urlopen(result_url)
    content =  resource.read().decode('utf-8')
    answer = json.loads(content)
    result = answer[0].get('sale')
    value = float(result)
    formatted_result = '{:5.2f}'.format(value)
    return formatted_result

# function for send back message
def send_message(chat_id, text):
    result_url = telegram_api_url + 'sendMessage'
    response = requests.post(result_url, json={'chat_id': chat_id, 'text': text})

# function to handle web hook
def handle_web_hook(request):
    answer = request.json
    message = answer.get('message')
    log_str = 'Some request have come, but not recognized.'
    if message != None:
        chat = message.get('chat')
        if chat != None:
            username = chat.get('username')
            chat_id = chat.get('id')
            text = message.get('text')
            log_str = '%s: %s' % (username, text)
            answer_message = 'USD currency is: %s' % parse_urd_current()
            send_message(chat_id, answer_message)
    log_data.append(log_str)

# route for main page
@app.route('/')
def log():
    return render_template('log.html')

# route for stats
@app.route('/stats/<id>')
def stats(id):
    offset = int(id)
    result = log_data[offset:]
    if result == None:
        result = []
    return json.dumps(result)

#rotue for telegram web hook
@app.route(hook_url_path, methods=['POST'])
def hook():
    if request.method == 'POST':
        handle_web_hook(request)
    return '';

# try to set webhook
if set_web_hook() == False:
    print('Error with setting up telegram wep hook.')
    sys.exit()

# run apllication
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/mia-currency-tbot.jakeroid.com/fullchain.pem', '/etc/letsencrypt/live/mia-currency-tbot.jakeroid.com/privkey.pem'))