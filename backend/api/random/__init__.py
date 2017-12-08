import json
import random

from twisted.internet import defer

from backend.api.utils import refine_twisted_web_request


class Random:
    def __init__(self):
        self._items = {}

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def random_get_all(self, request):
        print(request.args)
        r = yield defer.succeed(random.randint(1, 1000))
        defer.returnValue(json.dumps({
            'method'      : 'random_get_all',
            'randomNumber': r
        }))

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def random_get(self, request, id):
        r = yield defer.succeed(random.randint(1, 1000))
        defer.returnValue(json.dumps({
            'method'      : 'random_get',
            'randomNumber': r
        }))


def add_random_routes(app):
    random = Random()
    app.route('/api/random')(random.random_get_all)
    app.route('/api/random/<int:id>')(random.random_get)
