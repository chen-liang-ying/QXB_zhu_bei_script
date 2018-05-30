#!/usr/bin/env python
# coding: utf-8
# Author: liangying.chen
# Version: 1.0.0
# Date: 2018-05-29

import asyncio
from threading import Timer
import signal


def sig_handler(signame):
    print("got signal %s: exit" % signame)


class QxbClientProtocol(asyncio.Protocol):
    def __init__(self,loop):
        self.loop = loop
        signal.signal(signal.SIGTERM, sig_handler)

    def connection_made(self, transport):
        self.transport =transport
        print('connect server success')

        '定时处理扫描任务'
        self.timer = Timer(2,self.callback_work)
        self.timer.start()


    def data_received(self, data):
        mes = data.decode()
        print('Data received: {!r}'.format(mes))
        self.deal_mes(mes)

    def connection_lost(self, exc):
        print('The server closed the connection')
        if not self.timer.is_alive():
            print('Stop the event loop')
            self.timer.cancel()


    def data_send(self,data):
        mes = data.encode()
        self.transport.write(mes)

    def deal_mes(self,mes):
        if mes == 'heart':
            self.data_send(mes)
        else:
            print('recv error mesg')

    def callback_work(self):
        try:
            print('data_send 1')
            self.data_send('1')
            self.timer = Timer(2, self.callback_work)
            self.timer.start()
        except KeyboardInterrupt:
            print('data_send 0')
            self.data_send('0')




loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda: QxbClientProtocol(loop),
                              '127.0.0.1', 17693)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()




