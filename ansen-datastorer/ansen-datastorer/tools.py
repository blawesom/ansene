#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'

import os
import requests
import configparser
from sqlalchemy import func


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


def download_amd(amendement):

    # Path management
    raw_path = '/opt/ansene'
    storage_path = '/'.join([raw_path, 'storage'])
    if not os.path.exists(storage_path):
        os.mkdir(storage_path, mode=0o777)

    amd_path = '/'.join(["storage", str(amendement.project_id), str(amendement.exam_id)])
    if not os.path.exists('/'.join([raw_path, amd_path])):
        os.makedirs('/'.join([raw_path, amd_path]), mode=0o777)

    # Url build
    url_source = amendement.url[:-3] + 'pdf'
    file_name = '.'.join([amendement.amd_id, 'pdf'])
    target_file = '/'.join([raw_path, amd_path, file_name])

    # Get PDF file
    dl_state = download_pdf(url_source, target_file)
    if dl_state:
        amendement.downloaded = True

    return dl_state


def download_pdf(source, target):
    try:
        request = requests.get(source, stream=True)
        if request.status_code == 200:
            with open(target, 'wb') as filed:
                for chunk in request:
                    filed.write(chunk)
        return True
    except:
        return False
