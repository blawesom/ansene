# coding: utf-8

import requests
from flask import Flask, request, jsonify

import settings


app = Flask(__name__)

# - - - - - GENERAL - - - - -
@app.route('/')
def status():
    return jsonify({'Status': 'Alive'})


@app.route('/download', methods=['POST'])
def download_content():
    # TODO: Implement queuing for response if link is valid
    # TODO: Action to download file and POST to Storer, then delete local file

    url = request.form.get('url')
    amend_id = request.form.get('amend_id')
    response = requests.get(url)
    data = {'content': response.content,#'content': bytearray(response.content),
            'amend_id': amend_id,
            'url': url}
    requests.post("http://{}:{}/downloads/".format(settings.STORER['endpoint'], settings.STORER['port']), data=data)
    return jsonify({response.url: response.status_code})


if __name__ == "__main__":
    app.run(settings.API['endpoint'], int(settings.API['port']), debug=True)
