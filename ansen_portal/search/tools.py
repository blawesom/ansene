#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'

import configparser


def config():
    '''
    Read and return the configparser object based the config.ini next to it.

    :return: The opened config.ini file read by configparser
    :rtype: ConfigParser
    '''

    base_path = '/opt/ansene'
    cnf = configparser.ConfigParser()
    cnf.read(filenames='{0}/config.ini'.format(base_path))
    return cnf
