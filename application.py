from flask import Flask, url_for, render_template, request
import json
import urllib.request
from bs4 import BeautifulSoup
from config import getConfig

app = Flask(__name__, static_folder='static', static_url_path='')

config = getConfig()

telegramApiUrl = "https://api.telegram.org/bot%s/" % config.get('telegramBotApiToken')
hookUrlPath = '/hook/%s' % config.get('telegramBotApiToken')
hookUrl = 'https://mia-currency-tbot.jakeroid.com%s' % hookUrlPath

logData = [];

def setWebHook():

    return

def parseUsdCurrency():
    data = urllib.request.urlopen('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5').read()
    answer = json.loads(data)
    result = answer[0].get('sale')
    return result

@app.route('/')
def log():
    return render_template('log.html')

@app.route('/stats')
def stats():
    result = []
    while len(logData) > 0:
        elem = logData.pop(-1)
        result.append(elem)
    return json.dumps(result)

@app.route(hookUrlPath, methods=['POST'])
def hook():
    if request.method == 'POST':
        print(request.json)
        currency = parseUsdCurrency()
        logString = 'This is example of log string. Currency %s.' % currency;
        logData.append(logString)
    return '';

if __name__ == "__main__":
    app.run()