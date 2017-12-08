import json
import sqlite3

from pypika import Table, Query
from twisted.internet import defer

from backend.api.utils import refine_twisted_web_request
from backend.database import data_db_conn


class Users:
    def __init__(self):
        self._items = {}
        self.table = Table('Users')

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def user_get_all(self, request):
        print(request.args)
        r = yield defer.succeed({'method': 'user_get_all'})
        defer.returnValue(json.dumps(r))

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def user_get(self, request, id):
        print(request.args)
        r = yield defer.succeed({'method': 'user_get'})
        defer.returnValue(json.dumps(r))

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def user_create(self, request):
        user = json.load(request.content)
        try:
            yield data_db_conn.runOperation(str(
                Query.into(self.table).columns('uid', 'name', 'desc').insert(user['email'], user['name'],
                                                                             user['select'])))
        except sqlite3.IntegrityError:
            defer.returnValue(json.dumps({'success': False, 'reason': '이미 등록된 고객정보 입니다.'}))
        except:
            raise
        defer.returnValue(json.dumps({'success': True}))

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def user_update(self, request, id):
        print(request.args)
        r = yield defer.succeed({'method': 'user_update'})
        defer.returnValue(json.dumps(r))

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def user_delete(self, request, id):
        print(request.args)
        r = yield defer.succeed({'method': 'user_delete'})
        defer.returnValue(json.dumps(r))


def add_users_routes(app):
    users = Users()
    app.route('/api/users', methods=['GET'])(users.user_get_all)
    app.route('/api/users/<string:id>', methods=['GET'])(users.user_get)
    app.route('/api/users', methods=['POST'])(users.user_create)
    app.route('/api/users/<string:id>', methods=['PUT'])(users.user_update)
    app.route('/api/users/<string:id>', methods=['DELETE'])(users.user_delete)
