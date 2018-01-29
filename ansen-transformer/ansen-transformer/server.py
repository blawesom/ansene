#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import flask
import json
import tools


app = flask.Flask(__name__)

@app.route('/')
def status():
    return json.dumps({ 'Service': 'transformer',
                        'Status': 'Alive'})


if __name__ == '__main__':
    hostname = tools.config().get(section='transformer', option='server')
    port = tools.config().get(section='transformer', option='port')

    app.run(host='0.0.0.0', port=int(port), debug=True)
