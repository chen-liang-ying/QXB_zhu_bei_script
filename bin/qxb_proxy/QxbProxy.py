#!/usr/bin/env python
# coding: utf-8
# Author: liangying.chen
# Version: 1.0.0
# Date: 2018-05-29


class QxbProxy(object):

    def __init__(self):
        print('init QxbProxy')
        self.client = []

    def addClient(self, client):
        self.client.append(client)

    def removeClient(self,client):
        self.client.remove(client)

    def sendData(self,mes,client):
        client.data_write(mes)

    def rec_data(self,mes,client):
        client.dealRecMes(mes)

