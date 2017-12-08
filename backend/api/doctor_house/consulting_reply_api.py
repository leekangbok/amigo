import collections
import io
import json
from operator import attrgetter

import jsonpickle
from pypika import Table, enums
from twisted.internet import defer
from twisted.logger import jsonFileLogObserver, Logger

from backend.api.utils import refine_twisted_web_request
from backend.database.model.consulting import ConsultingReply
from backend.database.model.model_base import ModelResponse, ModelRequest, ModelDeleteRequest
from backend.database.model.model_base import get_model_request_args
from backend.database.sqlite3_base import SQLite3JsonBase, get_sqlite3_column_name


class ConsultingReplyApi(SQLite3JsonBase):
    log = Logger(observer=jsonFileLogObserver(io.open("log.json", "a")), namespace="ConsultingReply")

    table_fields = ' '.join(get_sqlite3_column_name('ConsultingReply'))
    table_fields_getter = attrgetter(*table_fields.split())
    row_named_record = collections.namedtuple('ConsultingReply',
                                              ' '.join([SQLite3JsonBase.table_common_fields, table_fields]))

    def __init__(self):
        self.table = Table('ConsultingReply')

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_reply_get_all(self, request):
        resp = yield self.search_service_execute(
                ModelRequest(*get_model_request_args(request.args),
                             item=ConsultingReply(uid=request.args.get('uid', [''])[0],
                                                  consulting_uid=request.args.get('consulting_uid', [''])[0])))
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_reply_get(self, request, uid):
        resp = yield self.search_service_execute(
                ModelRequest(*get_model_request_args(request.args), item=ConsultingReply(uid=uid)))
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_reply_create(self, request):
        content = json.load(request.content)
        resp = yield self.update_service_execute(
                ModelRequest(*get_model_request_args(request.args), item=ConsultingReply(**content)))
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_reply_delete(self, _, uid):
        resp = yield self.delete_service_execute(ModelDeleteRequest(uid))
        return jsonpickle.encode(resp, unpicklable=False)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def consulting_reply_update(self, request, uid):
        content = json.load(request.content)
        content['uid'] = uid
        resp = yield self.update_service_execute(
                ModelRequest(*get_model_request_args(request.args), item=ConsultingReply(**content)))
        return jsonpickle.encode(resp, unpicklable=False)

    @staticmethod
    def create_response(**kwd):
        return ModelResponse(ConsultingReply)

    @staticmethod
    def set_sortby_statement(q, req):
        q = super(ConsultingReplyApi, ConsultingReplyApi).set_sortby_statement(q, req)
        q = q.orderby('reg_date', order=enums.Order.desc)
        return q

    def set_keyword_statement(self, q, req):
        if req.item.consulting_uid:
            q = q.where(self.table.consulting_uid == req.item.consulting_uid)
        if req.item.author:
            q = q.where(self.table.author == req.item.author)
        return q


def add_doctor_house_consulting_reply_routes(app):
    api = ConsultingReplyApi()
    app.route('/api/doctor/consulting_reply', methods=['GET'])(api.consulting_reply_get_all)
    app.route('/api/doctor/consulting_reply/<string:uid>', methods=['GET'])(api.consulting_reply_get)
    app.route('/api/doctor/consulting_reply', methods=['POST'])(api.consulting_reply_create)
    app.route('/api/doctor/consulting_reply/<string:uid>', methods=['DELETE'])(api.consulting_reply_delete)
    app.route('/api/doctor/consulting_reply/<string:uid>', methods=['PUT'])(api.consulting_reply_update)
