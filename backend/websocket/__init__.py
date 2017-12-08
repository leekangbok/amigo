import json
import random

import txaio
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from twisted.internet import reactor
from twisted.internet import task

factory = None


def update_wait_user(user):
    for user_tmp in factory.items:
        if user_tmp['uid'] == user['uid']:
            user_tmp['state'] = user['state']
            for c in factory.open_connections:
                c.sendMessage(json.dumps({'mutation'   : 'ws/dental/wait/welcome/set',
                                          'welcome'    : True,
                                          'currentName': user['name']
                                          }).encode(), False)
                if factory.items:
                    c.sendMessage(json.dumps({'mutation': 'ws/livestream/append',
                                              'data'    : factory.items,
                                              'total'   : len(factory.items),
                                              }).encode(), False)
            break


def append_wait_user(user):
    user.update(uid=random.randint(0, 999999999))
    factory.items.append(user)
    for pri, c in enumerate(factory.items, 1):
        c.update(pri=pri)


def delete_wait_user(uid):
    factory.items = [i for i in factory.items if i['uid'] != uid]
    for pri, c in enumerate(factory.items, 1):
        c.update(pri=pri)
    for c in factory.open_connections:
        c.sendMessage(json.dumps({'mutation': 'ws/livestream/delete', 'uid': uid}).encode(), False)
    for c in factory.open_connections:
        if factory.items:
            c.sendMessage(json.dumps({'mutation': 'ws/livestream/append',
                                      'data'    : factory.items,
                                      'total'   : len(factory.items),
                                      }).encode(), False)


def get_wait_user():
    return factory.items


class MyServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.is_closed = txaio.create_future()
        self.send = None
        self.start = 0
        self.limit = 1

    def send_item(self):
        item = self.factory.items[self.start:self.start + self.limit]
        if item:
            self.sendMessage(json.dumps({'mutation': 'ws/livestream/append',
                                         'data'    : item,
                                         'total'   : len(self.factory.items),
                                         }).encode(), False)
            self.start += 1
        else:
            self.start = 0

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        self.factory.open_connections.append(self)

        self.sendMessage(json.dumps({'mutation': 'ws/dental/wait/all/users/append',
                                     'data'    : self.factory.items,
                                     }).encode(), False)

        self.send = task.LoopingCall(self.send_item)
        self.send.start(3, 0)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(json.dumps({'mutation': 'SOCKET_TEST', 'hello': 'world'}).encode(), isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.open_connections.remove(self)
        if self.send is not None:
            self.send.stop()


def web_socket_run(host, port):
    global factory
    factory = WebSocketServerFactory(u"ws://0.0.0.0:{}".format(port))
    # factory.setProtocolOptions(
    #         allowedOrigins=[
    #             "http://localhost:9000",
    #             "http://localhost:8080",
    #         ],
    #         allowNullOrigin=True
    # )
    factory.protocol = MyServerProtocol
    factory.items = []
    factory.open_connections = []

    reactor.listenTCP(port, factory)
