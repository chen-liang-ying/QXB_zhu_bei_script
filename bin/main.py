#!/usr/bin/env python
# coding: utf-8
# Author: liangying.chen
# Version: 1.0.0
# Date: 2018-05-29

import asyncio
from qxb_ServerProtocol.QxbServerProtocol import QxbServerProtocol

def create_tcp_s():
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    # sProtocol = QxbServerProtocol(loop)
    'have to use -->lambda:QxbServerProtocol(loop) not use QxbServerProtocol(loop),' \
    'the reason i does not konw'

    coro = loop.create_server(lambda:QxbServerProtocol(loop), '127.0.0.1', 17693)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        print('20')
        loop.run_forever()
        print('22')
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    print('28')
    loop.run_until_complete(server.wait_closed())
    loop.close()

def main():
    '创建tcp服务端'
    create_tcp_s()

if __name__ == '__main__':
    main()