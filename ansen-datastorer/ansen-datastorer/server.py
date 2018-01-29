#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import flask
import tools
import models
import dbhandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


app = flask.Flask(__name__)

# ------ DB setup ------

db_host = tools.config().get(section='postgre', option='server')
db_port = tools.config().get(section='postgre', option='port')
db_user = 'datastorer'
db_pwd = 'benjamin'
db_name = 'ansene'

engine = create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(db_user, db_pwd, db_host, db_port, db_name))

models.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
conn = Session()


# ------ Web Server ------

@app.route('/')
def status():
    return flask.jsonify({  'Service': 'datastorer',
                            'Status': 'Alive'})


@app.route('/an', methods=['GET'])
def get_an_projs():
    all_projects, all_cats, all_names = dbhandler.get_docs(conn, orga='AN')
    if all_projects:
        return flask.jsonify({'all_projects': list(all_projects),
                              'all_cats': list(all_cats),
                              'all_names': list(all_names)})
    else:
        return flask.jsonify({'all_projects': []})


@app.route('/an', methods=['POST'])
def put_documents():
    write_conn = Session()
    action = dbhandler.add_doc(session=write_conn, data=flask.request.get_json())
    write_conn.close()
    return flask.jsonify(str(action))


@app.route('/an/<proj_id>', methods=['GET'])
def get_an_exams(proj_id):
    all_exams = dbhandler.get_docs(conn, orga='AN', project_id=proj_id)
    return flask.jsonify({'all_exams': all_exams})


@app.route('/an/<proj_id>/<exam_id>', methods=['GET'])
def get_an_amds(proj_id, exam_id):
    all_amds = dbhandler.get_docs(conn, orga='AN', project_id=proj_id, exam_id=exam_id)
    return flask.jsonify({'all_amds': all_amds})


@app.route('/an/<proj_id>/<exam_id>/<amd_id>', methods=['GET'])
def get_an_amd(proj_id, exam_id, amd_id):
    amd = dbhandler.get_docs(conn, orga='AN', project_id=proj_id, exam_id=exam_id, amd_id=amd_id)
    return flask.jsonify(amd)


# ------ Run Server ------


if __name__ == '__main__':
    hostname = tools.config().get(section='storer', option='server')
    port = tools.config().get(section='storer', option='port')

    app.run(host='0.0.0.0', port=int(port), debug=True)
