import collections
import io
import json
from operator import attrgetter

import jsonpickle
from pypika import Table
from pypika import enums
from twisted.internet import defer
from twisted.logger import jsonFileLogObserver, Logger

from backend.api.doctor_house.consulting_reply_api import ConsultingReplyApi
from backend.api.utils import refine_twisted_web_request
from backend.database.model.consulting import Consulting
from backend.database.model.model_base import ModelResponse, ModelRequest, ModelDeleteRequest, TwistedRequestWrapper
from backend.database.model.model_base import get_model_request_args
from backend.database.sqlite3_base import SQLite3JsonBase, get_sqlite3_column_name


class ConsultingApi(SQLite3JsonBase):
    log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")), namespace="Consulting")

    table_fields = ' '.join(get_sqlite3_column_name('Consulting'))
    table_fields_getter = attrgetter(*table_fields.split())
    row_named_record = collections.namedtuple('Consulting',
                                              ' '.join([SQLite3JsonBase.table_common_fields, table_fields]))

    def __init__(self):
        self.table = Table('Consulting')

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_get_all(self, request):
        resp = yield self.search_service_execute(
                ModelRequest(*get_model_request_args(request.args),
                             item=Consulting(uid=request.args.get('uid', [''])[0],
                                             subject=request.args.get('subject', [''])[0],
                                             body=request.args.get('body', [''])[0],
                                             author=request.args.get('author', [''])[0])))
        yield self.set_reply_item(resp.items)
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_get(self, request, uid):
        resp = yield self.search_service_execute(
                ModelRequest(*get_model_request_args(request.args), item=Consulting(uid=uid)))
        yield self.set_reply_item(resp.items)
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_create(self, request):
        content = json.load(request.content)
        item = Consulting(**content)
        item.clicked = 0
        resp = yield self.update_service_execute(
                ModelRequest(*get_model_request_args(request.args), item=item))
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_delete(self, _, uid):
        resp = yield self.delete_service_execute(ModelDeleteRequest(uid))
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_update(self, request, uid):
        content = json.load(request.content)
        content['uid'] = uid
        resp = yield self.update_service_execute(
                ModelRequest(*get_model_request_args(request.args), item=Consulting(**content)),
                module='consulting_update')

        return jsonpickle.encode(resp, unpicklable=False)

    def set_keyword_statement(self, q, req):
        c = self.set_like_keyword_statement(None, req.item.subject, self.table.subject)
        c = self.set_like_keyword_statement(c, req.item.body, self.table.body)
        c = self.set_like_keyword_statement(c, req.item.author, self.table.author)
        if c is not None:
            q = q.where(c)
        return q

    @staticmethod
    def set_sortby_statement(q, req):
        q = super(ConsultingApi, ConsultingApi).set_sortby_statement(q, req)
        q = q.orderby('reg_date', order=enums.Order.desc)
        return q

    @staticmethod
    def create_response(**kwd):
        return ModelResponse(Consulting)

    @defer.inlineCallbacks
    def set_reply_item(self, items):
        api = ConsultingReplyApi()
        o = TwistedRequestWrapper()
        for item in items:
            item.reply = []
            o.args['consulting_uid'] = [item.uid]
            api_ret = yield api.consulting_reply_get_all(o)
            api_ret = json.loads(api_ret)
            item.reply.extend(api_ret['items'])


def add_doctor_house_consulting_routes(app):
    api = ConsultingApi()
    app.route('/api/doctor/consulting', methods=['GET'])(api.consulting_get_all)
    app.route('/api/doctor/consulting/<string:uid>', methods=['GET'])(api.consulting_get)
    app.route('/api/doctor/consulting', methods=['POST'])(api.consulting_create)
    app.route('/api/doctor/consulting/<string:uid>', methods=['DELETE'])(api.consulting_delete)
    app.route('/api/doctor/consulting/<string:uid>', methods=['PUT'])(api.consulting_update)
