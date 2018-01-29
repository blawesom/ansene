# coding: utf-8

from configparser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')

API_URL = "http://" + ":".join([conf['storer']['server'], conf['storer']['port']])

API = {'endpoint': '0.0.0.0',  # conf['ui']['server'],
       'port': conf['ui']['port']}