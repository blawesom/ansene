# coding: utf-8

from configparser import ConfigParser

conf = ConfigParser()
conf.read('config.ini')

MONGODB = {'endpoint': conf['mongodb']['server'],
           'port': conf['mongodb']['port']}

API = {'endpoint': '0.0.0.0',               # conf['storer']['server'],
       'port': conf['storer']['port']}
