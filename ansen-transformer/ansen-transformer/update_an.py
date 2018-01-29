#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import time
import requests
from tools import config, cat_projet, specify, get_no
from distributer import celeri
import logging
from logging.handlers import RotatingFileHandler


# Configurer logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Configure output format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Configure the handler, max size: 50 MB
file_handler = RotatingFileHandler('/var/log/ansene/transformer_error.log', 'a+', 50000000)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# logger.error('Type error because: {0}'.format(err))


def main():
    '''
    Update the data from the storer, pulling everything needed (projects, exams, amds) to compare and qualify.

    :return: Status of the operation
    :rtype: dict
    '''

    logger.debug('Getting fresh data...')
    data_now = get_an_state(source='crawler')
    logger.debug('Getting old data...')
    data_past = get_an_stored(source='storer')
    logger.debug('Comparing data...')
    diff = compare_an(data_now['all_exams'], data_past['all_exams'])
    logger.debug('Pulling differential...')
    data_new = []
    for exam in diff:
        new = get_new_amd.delay(exam)
        data_new.append(new)

    pushed = []
    while len(data_new) > 0:
        for data in data_new:
            if data.ready():
                for amd in data.get():
                    pushing = push_an.delay('storer', amd)
                    pushed.append(pushing)
                data_new.pop(data_new.index(data))
            else:
                time.sleep(0.1)
    logger.debug('Operation ended with success.')
    return {'Status': 'Operation finished with success'}


def pull_an(source, proj_id=None, exam_id=None):
    '''
    Wrapper for data pulling from Storer or Crawler.

    :param source: Service provider for the info pulled: 'storer' or 'crawler'
    :type source: str
    :param proj_id: Reference ID of the project.
    :type proj_id: str
    :param exam_id: Reference ID of the exam.
    :type exam_id: str
    :return: Raw data provided by the service called
    :rtype: dict
    '''

    host = config().get(section=source, option='server')
    port = config().get(section=source, option='port')
    hostname = '{0}:{1}'.format(host, port)
    data = {"list_n_project": [],
            "list_project": [],
            "all_exams": [],
            "all_amds": [],
            }
    if proj_id:
        if exam_id:
            data0 = requests.get(url='http://{0}/an/{1}/{2}'.format(hostname, proj_id, exam_id))
            try:
                data = data0.json()
            except Exception as err:
                logger.error('Error pulling amd:\t{} -\t{}'.format(err, data0.content))
        else:
            data0 = requests.get(url='http://{0}/an/{1}'.format(hostname, proj_id))
            try:
                data = data0.json()
            except Exception as err:
                logger.error('Error pulling exam:\t{} -\t{}'.format(err, data0.content))
    else:
        data0 = requests.get(url='http://{0}/an'.format(hostname))
        try:
            data = data0.json()
        except Exception as err:
            logger.error('Error pulling amd:\t{} -\t{}'.format(err, data0.content))

    return data


@celeri.task(name='task.push_amd')
def push_an(dest, amd):
    '''
    Wrapper for data pushing toward the Storer.

    :param dest: Service hoster for the info received: 'storer'
    :type dest: str
    :param amd: Amendment to be added to the destination service
    :type amd: dict
    :return: Code status
    :rtype: str
    '''

    host = config().get(section=dest, option='server')
    port = config().get(section=dest, option='port')
    hostname = '{}:{}'.format(host, port)
    status = requests.post(url='http://{0}/an'.format(hostname), json=amd)
    return status.content


def get_an_state(source):
    '''
    Get the basic infos of all the project, exams and number of amendments within from the crawler

    :param source: Service provider for the info available online: 'crawler'
    :type source: str
    :return: Exam with ID, project parent ID and nb of amendments in a dict.
    :rtype: dict
    '''
    return_data = []
    pulled_data = pull_an(source=source)
    # limited pull for test purposes (add [:3]) for partial pull
    for proj_id in pulled_data['list_n_project']:
        exam_list = pull_an(source=source, proj_id=proj_id)['all_exams']
        for exam in exam_list:
            return_data.append({
                                'project_id': proj_id,
                                'exam_id': exam['exam_id'],
                                'nb_amd' : exam['nb_amd']
                                })
    return {'all_exams': return_data}


def get_an_stored(source):
    '''
    Get the basic infos of all the project, exams and number of amendments within from the storer

    :param source: Service provider for the info available online: 'crawler'
    :type source: str
    :return: Exam with ID, project parent ID and nb of amendments in a dict.
    :rtype: dict
    '''
    return_data = []
    pulled_data = pull_an(source=source)
    for project in pulled_data['all_projects']:
        exam_list = pull_an(source=source, proj_id=project)
        for exam in exam_list['all_exams']:
            return_data.append({
                                'project_id': project,
                                'exam_id'   : exam['exam_id'],
                                'nb_amd'    : exam['nb_amd']
                                })
    return {'all_exams': return_data}


@celeri.task(name='task.get_new_amd')
def get_new_amd(exam):
    '''
    Pull all the amendments within an exam, from crawler and storer and returns only the new ones.

    :param exam: Exam ID to check for.
    :type exam: str
    :return: Only new amendments of the listed exams.
    :rtype: list
    '''
    return_data = []

    old = pull_an(source='storer', proj_id=exam['project_id'], exam_id=exam['exam_id'])
    fresh = pull_an(source='crawler', proj_id=exam['project_id'], exam_id=exam['exam_id'])
    new = format_amds(proj_id=exam['project_id'],  exam_id=exam['exam_id'], full_exam_data=fresh)
    for amd in new:
        if amd['amd_id'] not in old:
            return_data.append(amd)
    return return_data


def format_amds(proj_id, exam_id, full_exam_data):
    '''
    Format and qualify the amendments to be stored.

    :param proj_id: Reference ID of the project.
    :type proj_id: str
    :param proj_title: Full eader title for the project.
    :type proj_id: str
    :param exam_id: Reference ID of the exam.
    :type exam_id: str
    :param full_exam_data: Raw data from the crawler describing the amendments
    :type: str
    :return: Qualified and formated amendments in dict.
    :rtype: list
    '''
    amd_list = []
    return_list = []


    header = 'id|numInit|titreDossierLegislatif|urlDossierLegislatif|instance|numAmend|urlAmend|designationArticle|'\
             'designationAlinea|dateDepot|signataires|sort|missionVisee'
    headers = header.split('|')
    for raw_amd in full_exam_data['all_amds']:
        clean_amd = dict(zip(headers, raw_amd.split('|')))
        amd_list.append(clean_amd)

    for amd in amd_list:
        s_type = specify(url=amd['urlAmend'])
        nb = get_no(indication=amd['designationArticle'])
        categorie, nom = cat_projet(amd['titreDossierLegislatif'])
        formated_amd = {
                            'organisme'     : 'AN',
                            'project_id'    : proj_id,
                            'project_cat'   : categorie,
                            'project_name'  : nom,
                            'exam_id'       : exam_id,
                            'exam_name'     : '',
                            'amd_id'        : amd['id'],
                            's_type'        : s_type,
                            'url'           : amd['urlAmend'],
                            'n_article'     : nb,
                            'sort'          : amd['sort'],
                            'signataires'   : amd['signataires'],
                        }
        return_list.append(formated_amd)
    return return_list


def compare_an(data_now, data_past):
    '''
    Check and select modified (new or with new amendment)

    :param data_now: Basic infos of all the project, exams and number of amendments, pulled online
    :type data_now: list
    :param data_past: Basic infos of all the project, exams and number of amendments stored.
    :type data_past: list
    :return:  New or modified exams
    :rtype: list
    '''
    return_list = []

    for exam in data_now:
        if exam not in data_past:
            logger.info('New data to pull: {}'.format(exam))
            return_list.append(exam)

    return return_list


# def refresh_ppl():
#     list_ppl = []
#
#     depute_liste = get_all()['ppl_list']
#     for depute in depute_liste:
#         url, nom = depute
#         list_ppl.append(get_ppl(url=url, name=nom))
#
#     return {'all_ppl': list_ppl}


if __name__ == '__main__':
    main()
