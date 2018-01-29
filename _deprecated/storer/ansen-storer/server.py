# coding: utf-8
from flask import Flask, jsonify, request

import json
import settings
import db

app = Flask(__name__)
conn = db.MongoConnection()


@app.route('/', methods=['GET'])
def status():
    return json.dumps({'Status': 'Alive'})


@app.route('/an', methods=['GET'])
def get_all_projects(document_type='exam', connection=conn):
    docs = dict()
    docs['all_{}s'.format(document_type)] = conn.get_all_documents(document_type)
    docs['{}s_count'.format(document_type)] = len(docs['all_{}s'.format(document_type)])
    return jsonify(docs)


@app.route('/an/<project_id>/', methods=['GET'])
def get_exams_from_project(project_id, connection=conn):
    docs = connection.get_all_documents('exam', filter={'project_id': project_id})
    resp = {'all_exams': docs, 'count': len(docs)}
    return jsonify(resp)


@app.route('/an/<project_id>/<exam_id>', methods=['GET'])
def get_amends_from_exam(project_id, exam_id, connection=conn):
    docs = connection.get_all_documents('amend', filter={'project_id': project_id,
                                                         'exam_id': exam_id}, )
    resp = {'all_amends': docs, 'count': len(docs)}
    return jsonify(resp)



@app.route('/<document_type>s/', methods=['GET'])
def get_all_documents(document_type, connection=conn):
    docs = dict()
    docs['all_{}s'.format(document_type)] = conn.get_all_documents(document_type)
    docs['{}s_count'.format(document_type)] = len(docs['all_{}s'.format(document_type)])
    return jsonify(docs)


@app.route('/<document_type>s/', methods=['POST'])
def create_document(document_type, connection=conn):
    doc = db.generate_document_object(document_type, request.form)
    connection.insert_document(doc)
    return jsonify({"{}_id".format(document_type): getattr(doc, "{}_id".format(document_type))})

"""
@app.route('/<document_type>s/<document_id>/', methods=['GET'])
def get_document(document_type, document_id, connection=conn):
    doc = connection.get_document(document_type, document_id)
    return jsonify(doc)
"""


@app.route('/<document_type>s/<document_id>/', methods=['PUT'])
def update_document(document_type, document_id, connection=conn):
    doc = connection.update_document(document_type, document_id, request.form)
    return jsonify(doc)


if __name__ == "__main__":
    app.run(settings.API['endpoint'], int(settings.API['port']), debug=True)
