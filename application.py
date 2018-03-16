from flask import Flask, url_for, render_template, request
import json
import urllib.request
import requests
import sys
from config import getConfig

# prepare app object
app = Flask(__name__, static_folder='static', static_url_path='')

# main variables
config = getConfig()
telegramApiUrl = "https://api.telegram.org/bot%s/" % config.get('telegramBotApiToken')
hookUrlPath = '/hook/%s' % config.get('telegramBotApiToken')
hookAbsoluteUrl = 'https://mia-currency-tbot.jakeroid.com%s' % hookUrlPath
logData = [];

# set web hook function
def setWebHook():
    result_url = '%ssetWebHook?url=%s' % (telegramApiUrl, hookAbsoluteUrl)
    resource = urllib.request.urlopen(result_url)
    content =  resource.read().decode('utf-8')
    answer = json.loads(content)
    flag = answer.get('ok')
    return flag

# function for parse currency
def parseUsdCurrency():
    result_url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    resource = urllib.request.urlopen(result_url)
    content =  resource.read().decode('utf-8')
    answer = json.loads(content)
    result = answer[0].get('sale')
    value = float(result)
    formatted_result = '{:5.2f}'.format(value)
    return formatted_result

# function for send back message
def sendMessage(chat_id, text):
    result_url = telegramApiUrl + 'sendMessage'
    response = requests.post(result_url, json={'chat_id': chat_id, 'text': text})

# function to handle web hook
def handleWebHook(request):
    answer = request.json
    message = answer.get('message')
    log_str = 'Some request have come, but not recognized.'
    if message != None:
        chat = message.get('chat')
        if chat != None:
            username = chat.get('username')
            chat_id = chat.get('id')
            print(chat_id)
            text = message.get('text')
            log_str = '%s: %s' % (username, text)
            answer_message = 'USD currency is: %s' % parseUsdCurrency()
            sendMessage(chat_id, answer_message)
    logData.append(log_str)

# route for main page
@app.route('/')
def log():
    return render_template('log.html')

# route for stats
@app.route('/stats/<id>')
def stats(id):
    offset = int(id)
    result = logData[offset:]
    if result == None:
        result = []
    return json.dumps(result)

#rotue for telegram web hook
@app.route(hookUrlPath, methods=['POST'])
def hook():
    if request.method == 'POST':
        handleWebHook(request)
    return '';

# try to set webhook
if setWebHook() == False:
    print('Error with setting up telegram wep hook.')
    sys.exit()

# run apllication
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/mia-currency-tbot.jakeroid.com/fullchain.pem', '/etc/letsencrypt/live/mia-currency-tbot.jakeroid.com/privkey.pem'))