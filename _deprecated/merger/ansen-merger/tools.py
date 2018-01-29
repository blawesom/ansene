#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'


import time, os
from PyPDF2 import PdfFileMerger
from configparser import ConfigParser
import requests


def config():
    '''
    Read and return the configparser object based the config.ini next to it.

    :return: The opened config.ini file read by configparser
    :rtype: ConfigParser
    '''
    full_path = os.path.realpath(__file__)
    base_path = os.path.dirname(full_path)
    cnf = ConfigParser()
    cnf.read(filenames='{0}/config.ini'.format(base_path))
    return cnf


def get_files(pdf_list):
    '''
    Get a list of pdf from the storer

    :param pdf_list: List of full path of file to merge.
    :type pdf_list: list
    :return: Link to the file to download
    :rtype: str
    '''

    # pdf_list should be an array with full path for each files
    merged_export = PdfFileMerger()

    host = config().get(section='storer', option='server')
    port = config().get(section='storer', option='port')
    hostname = '{}:{}'.format(host, port)

    for file_path in pdf_list:
        # check if file already exists in
        # TODO: define protocol to pull file from the storer
        # http://source/orga/proj/exam/amd   {type:'pdf'}
        data = requests.get(url='http://{0}/file/'.format(hostname), json={'type', 'pdf'})



def merge_files(local_pdfs):
    '''
    Merge a list of pdf

    :param local_pdfs:
    :return:
    '''

    # save files in /tmp/ansene/merger/
    merged_export.append(open(file_path, 'rb'))

    raw_path = '/tmp/ansene/merger/'

    name = 'merge_{0}_output.pdf'.format(str(time.clock())[2:])
    output = open(raw_path + name, 'wb')
    merged_export.write(output)

    return "{0}{1}".format(raw_path, name)


def serve_file(path):

    # TODO: Store and serve file on unique link to be returned

    link = "http:/{0}".format(path)

    return link

