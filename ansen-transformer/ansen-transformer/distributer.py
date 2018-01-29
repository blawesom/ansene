#!/usr/bin/env python
# coding: utf-8
# __author__ = 'Benjamin'

from tools import config
from celery import Celery


rmq_ip = config().get(section='rabbitmq', option='server')
rmq_port = config().get(section='rabbitmq', option='port')

celeri = Celery('distributer',
                # user, password, hostname, port, vhost
                broker='amqp://worker:benjamin@{0}:{1}/ansene'.format(rmq_ip, rmq_port),
                backend='amqp://worker:benjamin@{0}:{1}//'.format(rmq_ip, rmq_port),
                include=['update_an'])


if __name__ == '__main__':
    celeri.start()
