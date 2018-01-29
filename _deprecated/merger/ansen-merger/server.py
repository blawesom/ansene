#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import flask
import json
import tools

app = flask.Flask(__name__)


@app.route('/')
def status():
    return json.dumps({'Status': 'Alive'})


@app.route('/files', methods=['POST'])
def merge_and_send(files):
    # Temps de process potentiellement long, attention au timeout de la requetes HTTP !
    # TODO: Request files (1 by 1) and merge it
    # TODO: Upload to goploader (depado or self hosted) an mail the link
    # TODO: Check timeout issues
    local_files = tools.get_files(files)
    new_file = tools.merge_files(local_files)
    new_link = tools.serve_file(new_file)
    return json.dumps({'link': new_link})


hostname = tools.config().get(section='merger', option='server')
port = tools.config().get(section='merger', option='port')

app.run(host='0.0.0.0', port=int(port), debug=True)
