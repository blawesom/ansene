import requests
from flask import Flask, render_template

import settings

app = Flask(__name__)

@app.route("/status")
def status():
    try:
        db_status = requests.get(settings.API_URL).json().get('status')
    except requests.ConnectionError as e:
        db_status = 'down'
    return render_template("status.html", content=db_status)
    
if __name__ == "__main__":
    app.run(settings.API['endpoint'], int(settings.API['port']), debug=True)
