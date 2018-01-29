#!/usr/bin/env python3
# coding: utf-8
# __author__ = 'Benjamin'

import os
import flask
import configparser

import an_amd
import an_ppl
import sen_amd


app = flask.Flask(__name__)

# ------ General ------
@app.route('/')
def status():
    return flask.jsonify({'Service': 'crawler',
                          'Status': 'Alive'})


# ------ Assemblee Nationale ------
@app.route('/an', methods=['GET'])
def crawl_an_proj():
    return flask.jsonify(an_amd.get_proj())


@app.route('/an/<proj_id>', methods=['GET'])
def crawl_an_exam(proj_id):
    return flask.jsonify(an_amd.get_exam(proj_id))


@app.route('/an/<proj_id>/<exam_id>', methods=['GET'])
def crawl_an_amd(proj_id, exam_id):
    return flask.jsonify(an_amd.get_amd(proj_id, exam_id))


@app.route('/ppl/an', methods=['GET'])
def crawl_an_ppl():
    return flask.jsonify(an_ppl.get_all())


@app.route('/ppl/an', methods=['POST'])
def get_an_ppl(data):
    return flask.jsonify(an_ppl.get_ppl(data['url'], data['name']))


# ------ Senat ------
@app.route('/sen', methods=['GET'])
def crawl_sen_proj():
    return flask.jsonify(sen_amd.get_proj())


@app.route('/ppl/sen', methods=['GET'])
def crawl_sen_ppl():
    return flask.jsonify({'url': 'url_test', 'name': 'name_test'})


# ------ Run Server ------

# full_path = os.path.realpath(__file__)
# base_path = os.path.dirname(full_path)

if __name__ == '__main__':
    base_path = '/opt/ansene'

    cnf = configparser.ConfigParser()
    cnf.read(filenames='{0}/config.ini'.format(base_path))
    hostname = cnf.get(section='crawler', option='server')
    port = cnf.get(section='crawler', option='port')

    app.run(host='0.0.0.0', port=int(port), debug=True)
