from flask import Flask, url_for, render_template
import json
app = Flask(__name__)

logData = ['Bla bla 1', 'TEST TEST', 'OHHOHHO'];

@app.route("/")
def log():
    stylesUrl = url_for('static', filename='styles.css')
    jqueryUrl = url_for('static', filename='jquery-3.3.1.min.js')
    scriptsUrl = url_for('static', filename='scripts.js')
    return render_template('log.html', stylesUrl=stylesUrl, jqueryUrl=jqueryUrl, scriptsUrl=scriptsUrl)

@app.route("/stats")
def stats():
    result = []
    while len(logData) > 0:
        print(len(logData))
        result.append(logData.pop())
    return json.dumps(result);


if __name__ == "__main__":
    app.run()