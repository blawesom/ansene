#!/usr/bin/env python3
# coding: utf-8
# __author__ = 'Benjamin'


import requests
from bs4 import BeautifulSoup
import re


def get_all():
    '''
    Get all députés.

    :return: List of tuple containing names and link to profile.
    :rtype: list
    '''

    # Récupération de la liste des députés
    base_url = 'http://www2.assemblee-nationale.fr/deputes/liste/tableau'
    page = requests.post(base_url)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    result_list = [(row.a['href'], row.a.text) for row in rows]

    return {'ppl_list': result_list}


def get_ppl(url, name):

    base_url = 'http://www2.assemblee-nationale.fr/'
    page = requests.get(''.join((base_url, url)))
    soup = BeautifulSoup(page.content, 'lxml')
    data = soup.find('div', {'id': 'haut-contenu-page'})

    bandeau = data.find('div', {'class': 'titre-bandeau-bleu'})
    attributs = data.find('dl', {'class': 'deputes-liste-attributs'})

    titres = name.split(' ')
    circo = bandeau.find('p', {'class': 'deputy-healine-sub-title'})
    datas = attributs.find_all('li')

    regex = re.compile(r'[\n\r\t]')

    fiche = {'genre': titres[0],
             'prenom': titres[1],
             'nom': ' '.join(titres[2:]),
             'mandat': circo.text,
             'commission': datas[0].text,
             'naissance': regex.sub('', datas[1].text),
             'mail': datas[4].a['href'].split(':')[1],
             'parti': regex.sub('', datas[6].text),
             'suppleant': datas[3].text}

    return fiche
