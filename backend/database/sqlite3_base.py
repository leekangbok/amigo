import sqlite3
from abc import ABC, abstractmethod
from functools import reduce
from itertools import dropwhile
from operator import attrgetter
from time import time
from types import MappingProxyType

from pypika import Query, enums
from twisted.internet import defer

from backend.database import data_db, data_db_conn
from backend.misc import generate_random_bits
from backend.misc.exception_base import serv_err_handler


def get_sqlite3_all_column_name(tablename):
    conn = sqlite3.connect(data_db)
    cursor = conn.cursor()
    cursor.execute('select * from {} limit 0'.format(tablename))
    for e in cursor.description:
        yield e[0]
    conn.close()


def get_sqlite3_column_name(tablename):
    conn = sqlite3.connect(data_db)
    cursor = conn.cursor()
    cursor.execute('select * from {} limit 0'.format(tablename))
    for _, e in dropwhile(lambda i: i[0] < 3, enumerate(cursor.description)):
        yield e[0]
    conn.close()


class SQLite3Base:
    db_handle = data_db_conn

    @staticmethod
    def fetch_recs_iter(cursor, fetch_size=100):
        while True:
            recs = cursor.fetchmany(fetch_size)
            if not recs:
                break
            for rec in recs:
                yield rec

    @staticmethod
    def fetchmany(cursor, query, cb):
        cursor.execute(query)
        return cb(SQLite3Base.fetch_recs_iter(cursor, 5))

    @staticmethod
    def fetchone(cursor, query, cb):
        cursor.execute(query)
        rec = cursor.fetchone()
        return cb(rec)

    @staticmethod
    def run_update(cursor, query):
        cursor.execute(query)
        return cursor.rowcount

    def run_fetch(self, query, callback):
        return self.db_handle.runInteraction(SQLite3Base.fetchmany, query, cb=callback)

    def run_query(self, query):
        return self.db_handle.runQuery(query)

    def run_operation(self, query):
        return self.db_handle.runInteraction(SQLite3Base.run_update, query)

    def run_interaction(self, interaction, *args, **kwargs):
        return self.db_handle.runInteraction(interaction, *args, **kwargs)


class SQLite3JsonBase(ABC, SQLite3Base):
    table_common_fields = "uid reg_date mod_date"
    table_common_fields_getter = attrgetter(*table_common_fields.split())

    @staticmethod
    def generate_uniq_uid():
        return generate_random_bits(64)

    def set_where_statement(self, q, req):
        if req.item.uid:
            q = q.where(self.table.uid == req.item.uid)
        return q

    @staticmethod
    def set_sortby_statement(q, req):
        if req.sortBy:
            q = q.orderby(req.sortBy,
                          order=enums.Order.desc if req.descending else enums.Order.asc)
        return q

    @staticmethod
    def set_offset_limit(q, req):
        # if req.rowsPerPage:
        #     q = q.limit(req.rowsPerPage)
        # if req.page:
        #     q = q.offset(req.page)
        return q

    def set_keyword_statement(self, q, req):
        return q

    def row_to_rec(self, row):
        return self.row_named_record(*row)

    def set_item_attr(self, item, rec, map_func=MappingProxyType({})):
        item.uid, item.reg_date, item.mod_date = self.table_common_fields_getter(rec)
        fields = self.table_fields.split()
        for field in fields:
            f = map_func.get(field)
            if f:
                f(item, getattr(rec, field))
            else:
                setattr(item, field, getattr(rec, field))

    def rec_to_item(self, item, rec):
        self.set_item_attr(item, rec)

    def column_values(self, item, map_func=MappingProxyType({})):
        columns = []
        for v in self.table_common_fields_getter(item):
            columns.append(v)
        fields = self.table_fields.split()
        if len(fields) > 1:
            for field in fields:
                f = map_func.get(field)
                v = getattr(item, field, None)
                columns.append(f(item, v) if f else v)
        else:
            f = map_func.get(fields[0])
            v = getattr(item, fields[0], None)
            columns.append(f(item, v) if f else v)
        return columns

    def build_sql_search(self, req, **kwd):
        wanted_select_fields = kwd.get('wsf', None)
        if wanted_select_fields is not None:
            q = Query.from_(self.table).select(*wanted_select_fields)
        else:
            q = Query.from_(self.table).select('*')
        q = self.set_where_statement(q, req)
        q = self.set_keyword_statement(q, req)
        q = self.set_sortby_statement(q, req)
        q = self.set_offset_limit(q, req)
        return defer.succeed(q)

    @defer.inlineCallbacks
    def search_query(self, req, **kwd):
        q = yield self.build_sql_search(req, **kwd)
        defer.returnValue(q)

    def build_sql_update(self, req, map_func=MappingProxyType({})):
        req.item.mod_date = int(time())

        if req.item.uid:
            q = Query.update(self.table)
            for n, (i, v) in enumerate(
                    zip(self.table_common_fields_getter(self.table), self.table_common_fields_getter(req.item)), 0):
                if n and v is not None:
                    q = q.set(i, v)
            fields = self.table_fields.split()
            if len(fields) > 1:
                for field, i in zip(fields, self.table_fields_getter(self.table)):
                    f = map_func.get(field)
                    v = getattr(req.item, field, None)
                    if v is not None:
                        q = q.set(i, f(req.item, v) if f else v)
            else:
                f = map_func.get(fields[0])
                v = getattr(req.item, fields[0], None)
                q = q.set(self.table_fields_getter(self.table), f(req.item, v) if f else v)
            q = q.where(self.table.uid == req.item.uid)
        else:
            req.item.uid = self.generate_uniq_uid()
            req.item.reg_date = int(time())
            q = Query.into(self.table)
            columns = self.column_values(req.item, map_func=map_func)
            q = q.insert(*columns)
        defer.returnValue(q)

    @defer.inlineCallbacks
    def update_query(self, req, **kwd):
        q = yield self.build_sql_update(req, map_func=kwd.get('map_func', {}))
        defer.returnValue(q)

    def build_sql_delete(self, uids):
        q = Query.from_(self.table)
        if uids:
            q = q.where(self.table.uid.isin(uids)).delete()
        else:
            q = q.delete()
        return defer.succeed(q)

    @defer.inlineCallbacks
    def delete_query(self, req, **_):
        q = yield self.build_sql_delete(list(req.items))
        defer.returnValue(q)

    @defer.inlineCallbacks
    def search_service_execute(self, req, **kwd):
        resp = self.create_response(**kwd)

        start = req.page
        limit = req.rowsPerPage
        match = kwd.get('match_func', lambda _: True)
        total = 0

        def fetch_all(it):
            nonlocal total
            for rec in (self.row_to_rec(i) for i in it):
                if match(rec):
                    if start <= total and resp.result.count < limit:
                        self.rec_to_item(resp.add(), rec)
                        resp.result.count += 1
                    total += 1
            return resp

        with serv_err_handler(resp, self.log, kwd.get('module', 'none')):
            q = yield self.search_query(req, **kwd)
            yield self.run_fetch(str(q).replace('REGEX', 'REGEXP'), callback=fetch_all)
            resp.result.total = total
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def update_service_execute(self, req, **kwd):
        resp = self.create_response(**kwd)

        with serv_err_handler(resp, self.log, kwd.get('module', 'none')):
            model = kwd.get('model', None)
            if model:
                columns = self.column_values(req.item, map_func=kwd.get('map_func', {}))
                model(*columns)

            in_loop, uid_origin = 0, req.item.uid
            while True:
                try:
                    q = yield self.update_query(req, **kwd)
                    yield self.run_operation(str(q))
                except sqlite3.IntegrityError:
                    req.item.uid = uid_origin
                    in_loop += 1
                    if in_loop > 100:
                        raise
                except:
                    raise
                else:
                    break
        defer.returnValue(resp)

    @defer.inlineCallbacks
    def delete_service_execute(self, req, **kwd):
        resp = self.create_response(**kwd)

        with serv_err_handler(resp, self.log, kwd.get('module', 'none')):
            q = yield self.delete_query(req, **kwd)
            yield self.run_operation(str(q))
        defer.returnValue(resp)

    @staticmethod
    @abstractmethod
    def create_response(**kwd):
        raise NotImplementedError

    @staticmethod
    def set_like_keyword_statement(s, t, attr):
        if not t:
            return s
        if isinstance(t, (str, bytes)):
            t = [t]
        n = reduce(lambda x, y: x | y, (attr.like(''.join(['%', str(e), '%'])) for e in t))
        if s is not None:
            s |= n
        else:
            s = n

        return s

    @staticmethod
    def set_regexp_keyword_statement(s, t, attr):
        if not t:
            return s
        if isinstance(t, (str, bytes)):
            t = [t]
        n = attr.regex('|'.join(str(e) for e in t))
        if s is not None:
            s |= n
        else:
            s = n

        return s
