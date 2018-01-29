#!/usr/bin/env python3
# coding: utf-8
# __author__ = 'Benjamin'


import re
import json
import math
import requests
from bs4 import BeautifulSoup


def get_proj():
    '''
    Get all project ids and text description.

    :return: Ids and Text description for each project as two list of equal length.
    :rtype: dict
    '''
    base_url = "http://www2.assemblee-nationale.fr/recherche/amendements"

    # Récupération de la liste des projets de loi
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, 'lxml')
    ladiv = soup.find('div', {'class': 'champs'})
    projets = ladiv.findAll('option')

    list_projet = [re.sub('"', '', option.text) for option in projets]  # remove double quote from project title
    list_n_projet = [option.attrs['value'] for option in projets]

    list_projet.pop(0)
    list_n_projet.pop(0)

    return {'list_n_project': list_n_projet, 'list_project': list_projet}


def get_exam(proj_id):
    '''
    Get all exams attached to a specific project.

    :param proj_id: Reference ID of the project.
    :type proj_id: str
    :return: Exams as dict containing ID and number of amendment attached to it.
    :rtype: dict
    '''
    list_exam = []

    # Récupération des examens pour le projet
    query_url = 'http://www2.assemblee-nationale.fr/recherche/query_amendements?typeDocument=amendement' \
                '&idDossierLegislatif={0}&typeRes=facettes'
    response = requests.get(query_url.format(proj_id))
    exam_data = response.json()

    for exam in exam_data['examenComposite']:
        query_sec = 'http://www2.assemblee-nationale.fr/recherche/query_amendements?typeDocument=amendement&idExamen=' \
                    '{0}&idDossierLegislatif={1}&missionVisee=&numAmend=&idAuteur=&idArticle=&idAlinea=&sort=' \
                    '&dateDebut=&dateFin=&periodeParlementaire=&texteRecherche=&rows=1&format=html&tri=ordreTexteasc&start=1&typeRes=liste'
        request_ex = requests.get(query_sec.format(exam['val'], proj_id))
        try:
            response_sec = request_ex.json()
        except:
            response_sec = sanitize(request_ex)

        nb_art = response_sec['infoGenerales']['nb_resultats']
        list_exam.append({'exam_id': exam['val'], 'nb_amd': nb_art})

    return {'all_exams': list_exam}


def get_amd(proj_id, exam_id):
    '''
    Get all amendments of a specific exam attached to the project.

    :param proj_id: Reference ID of the project.
    :type proj_id: str
    :param exam_id: Reference ID of the exam.
    :type exam_id: str
    :return: Amdendments as dict containing its raw data.
    :rtype: dict
    '''
    return_list = []

    # Récupération des amendements pour l'examen
    exam_url = 'http://www2.assemblee-nationale.fr/recherche/query_amendements?typeDocument=amendement&idExamen=' \
               '{0}&idDossierLegislatif={1}&missionVisee=&numAmend=&idAuteur=&idArticle=&idAlinea=&sort=' \
               '&dateDebut=&dateFin=&periodeParlementaire=&texteRecherche=&rows=500&format=html&tri=ordreTexteasc&start=1&typeRes=liste'

    answer = requests.get(exam_url.format(exam_id, proj_id))
    try:
        data = answer.json()
    except:
        data = sanitize(answer)

    nb_amd = data['infoGenerales']['nb_resultats']
    nb_page = int(math.ceil(nb_amd / 500))

    for page in range(nb_page):
        start_result = page * 500 + 1
        amd_url = 'http://www2.assemblee-nationale.fr/recherche/query_amendements?typeDocument=amendement&idExamen=' \
                  '{0}&idDossierLegislatif={1}&numAmend=&idAuteur=&idArticle=&idAlinea=&sort=&dateDebut=&dateFin=' \
                   '&periodeParlementaire=&texteRecherche=&rows=500&format=html&tri=ordreTexteasc&start={2}&typeRes=liste'
        amds = requests.get(amd_url.format(exam_id, proj_id, start_result))
        try:
            pulled_data = amds.json()
        except:
            pulled_data = sanitize(amds)

        for amd in pulled_data['data_table']:
            return_list.append(amd)

    return {'all_amds': return_list}


def sanitize(inidata):
    texte = inidata.text.encode('utf-8')
    split1 = texte.split(bytes('"texte_concerne" : "', 'utf-8'))
    split2 = split1[1].split(bytes('",\n"schema" :', 'utf-8'))
    split3 = split2[0].replace(bytes('"', 'utf-8'), bytes('', 'utf-8'))
    join2 = b'",\n"schema" :'.join([split3, split2[1]])
    join1 = b'"texte_concerne" : "'.join([split1[0], join2])
    data = json.loads(join1.decode('utf-8'))
    return data


# def clipboard()
#     repls = ('hello', 'goodbye'), ('world', 'earth')
#     s = 'hello, world'
#     reduce(lambda a, kv: a.replace(*kv), repls, s)
#     return