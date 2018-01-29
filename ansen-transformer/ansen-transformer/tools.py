#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'

import os, re
import requests
from lxml import html
import configparser


def config():
    '''
    Read and return the configparser object based the config.ini next to it.

    :return: The opened config.ini file read by configparser
    :rtype: ConfigParser
    '''
    # full_path = os.path.realpath(__file__)
    # base_path = os.path.dirname(full_path)
    base_path = '/opt/ansene'
    cnf = configparser.ConfigParser()
    cnf.read(filenames='{0}/config.ini'.format(base_path))
    return cnf


def cat_projet(proj):
    '''
    Detect and format a category and the name of the project.

    :param proj: Raw title of the project
    :type proj: str
    :return: Category (if available) and name of the project.
    :rtype: str, str
    '''
    temp_str = proj.translate({ord(c): " " for c in "\'\""})  # Removes .'. chars from string
    # p = re.compile('([A-Za-zéàèîïôêçû ’\-,]*)([: ]*)([ \(a-zA-Zéàèîïôêçû0-9’\-:,°\)]*)')
    pattern = re.compile('([A-Za-zéàèîïôêçû ’\-,]*)([: ]*)([ a-zA-Zéàèîïôêçû0-9’\-:,°]*)')

    if re.search(pattern, temp_str).group(2) != "":
        categorie = re.search(pattern, temp_str).group(1)
        nom = re.search(pattern, temp_str).group(3)
    else:
        categorie = " "
        nom = temp_str
    return categorie, nom

def specify(url):
    '''
    Parse and determine the article number and the special type of the amendment based on uts URL.

    :param url: Web page of the amendment
    :type url: str
    :param place: Check before put in prod
    :rtype: str
    :return: The article number (if possible) and the special type (rédactionnel...)
    :rtype: str, str
    '''

    page = requests.get(url)
    hmtl_tree = html.fromstring(page.text)

    list_redac = ['amendement rédactionnel', 'cet amendement a une portée rédactionnelle',
                  'amendement de précision rédactionnelle', 'amendement de cohérence rédactionnelle',
                  'amendement d’harmonisation rédactionnelle']
    list_irrecevable = ['amendement irrecevable au titre de', 'cet amendement a été déclaré irrecevable']
    list_retire = ['retiré avant discussion', 'cet amendement a été retiré avant séance']
    spec_typ = 'Aucun'

    champ = hmtl_tree.xpath(str('//*[@id="englobeOpen"]/dispositif/p/text()'))

    if True in [True in bool_list for bool_list in [[obj in line.lower() for obj in list_redac] for line in champ]]:
        spec_typ = 'redactionnel'
    if True in [True in bool_list for bool_list in
                [[obj in line.lower() for obj in list_irrecevable] for line in champ]]:
        spec_typ = 'irrecevable'
    if True in [True in bool_list for bool_list in
                [[obj in line.lower() for obj in list_retire] for line in champ]]:
        spec_typ = 'retire'

    return spec_typ


def get_no(indication):
    try:
        nb = [int(s) for s in indication.split() if s.isdigit()][-1]
        if 'Après' in indication:
            nb = str(nb + 1)
        else:
            nb = str(nb)
    except:
        if 'UNIQUE' in indication:
            nb='1'
        else:
            nb='Aucun'
    return nb


# def redecode(string):
#     table = ('\u00ea', 'ê'), ('\u00e9', 'é'), ('\u00e8', "è"), ('&#231;', 'ç'), ('&#232;', 'è')
#     return string