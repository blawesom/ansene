from django.shortcuts import render
import flask
# import requests
from . import tools, models
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


# Create your views here.
def search(request):
    return render(request, 'an_watch/newsearch.html',
                  {'tab_state': {'news': '',
                                 'recherche': '"active"',
                                 'alertes': '',
                                 'profil': ''}})


def projlist(request):
    list_proj = []
    allp =  conn.query(models.Amendement).\
            filter(models.Amendement.organisme == 'AN').\
            distinct(models.Amendement.project_id)
    for proj in allp:
        list_proj.append({'id': proj.project_id,
                          'cat': proj.project_cat,
                          'name': proj.project_name})

    return render(request, 'an_watch/projlist.html',
                  {'tab_state': {'news': '',
                                 'recherche': '"active"',
                                 'alertes': '',
                                 'profil': ''},
                    'project_list': list_proj})


def project(request, pid):
    alli = conn.query(models.Amendement). \
        filter(models.Amendement.project_id == pid)

    return render(request, 'an_watch/project.html',
                        {'tab_state': {'news': '',
                                       'recherche': '"active"',
                                       'alertes': '',
                                       'profil': ''},
                         'project': {'id': pid,
                                     'name': alli[0].project_name},
                         'item_list': alli})
