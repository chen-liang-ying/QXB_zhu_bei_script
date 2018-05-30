#!/usr/bin/env python
# coding: utf-8
# Author: liangying.chen
# Version: 1.0.0
# Date: 2018-05-29

import asyncio
from threading import Timer
from qxb_proxy.QxbProxy import QxbProxy

qxbProxy = QxbProxy()

class QxbServerProtocol(asyncio.Protocol):

    def __init__(self,loop):
        print('init QxbServerProtocol')
        self.heartCount = 0
        self.loop = loop

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

        '添加连接的客户端'
        qxbProxy.addClient(self)

        '此时创建heart'
        timer = Timer(3,self.sendHeart)
        timer.start()

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        qxbProxy.rec_data(message,self)

    def connection_lost(self, exc):
        qxbProxy.removeClient(self)
        print('stop loop')
        self.loop.stop()


    def data_send(self,mes):
        print('Send: {!r}'.format(mes))
        qxbProxy.sendData(mes,self)

    def data_write(self,data):
        mes = data.encode()
        self.transport.write(mes)

    def data_close(self):
        print('Close the client socket')
        self.transport.close()

    def sendHeart(self):
        if self.heartCount < 3:
            mes = 'heart'
            self.data_send(mes)
            self.heartCount = self.heartCount + 1
            timer = Timer(3, self.sendHeart)
            timer.start()
        else:
            '服务器关闭'
            self.data_close()
            self.loop.stop()

    def reset_heart(self):
        self.heartCount = 0

    def dealRecMes(self, message):
        '接收heart，不处理'
        '接受到“0”，拉起程序，关闭服务端'
        '接受到“1”，正常，pass'
        if message == '0':
            print('pull app')
        elif message == '1':
            print('pass')
        elif message == 'heart':
            print('heart')
            self.reset_heart()
        else:
            print('pull app')