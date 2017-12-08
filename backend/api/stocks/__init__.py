import json

from bs4 import BeautifulSoup
from treq import get
from twisted.internet import defer

from backend.api.utils import refine_twisted_web_request


class Stock:
    def __init__(self):
        self.stock_master = {}

    @defer.inlineCallbacks
    def stock_init(self):
        if self.stock_master:
            defer.returnValue(self.stock_master)
        r = yield get('http://www.financipe.com/api/stockmaster')
        r = yield r.text()
        self.stock_master = {i['stock_code']: {'stockName': i['stock_name']} for i in json.loads(r)}
        defer.returnValue(self.stock_master)

    @staticmethod
    def stock_per(stock, code):
        def on_complete(text, i):
            try:
                soup = BeautifulSoup(text, 'html.parser')
                per = soup.select('div.item-data2')
                per = per[0].select('tr td')
                per = float(per[0].text.strip())
                if stock:
                    stock['per'] = per
                return per
            except:
                return 0

        d = get('http://search.itooza.com/search.htm?seName={code}'.format(code=code))
        d.addCallback(lambda v: v.text()).addCallback(on_complete, stock)
        return d

    @staticmethod
    def stock_eps(stock, code):
        def on_complete(text, i):
            try:
                soup = BeautifulSoup(text, 'html.parser')
                eps = soup.select('div.sub_section table.tb_type1.tb_num.tb_type1_ifrs')
                eps = eps[0].select('tr td')
                eps1 = float(eps[92].text.strip().replace(',', ''))
                eps2 = float(eps[93].text.strip().replace(',', ''))
                if stock:
                    stock['eps1'] = eps1
                    stock['eps2'] = eps2
                return eps1, eps2
            except:
                return 0, 0

        d = get('http://finance.naver.com/item/main.nhn?code={code}'.format(code=code))
        d.addCallback(lambda v: v.text()).addCallback(on_complete, stock)
        return d

    @staticmethod
    def stock_sise(stock, code):
        def on_complete(text, i):
            soup = BeautifulSoup(text, 'html.parser')
            stock_rate = soup.select('ul.list_stockrate')
            try:
                if stock_rate:
                    cur_price = stock_rate[0].select('em.curPrice')
                    if cur_price:
                        i['curPrice'] = cur_price[0].text.strip()
                        i['down'] = True if cur_price[0]['class'][1] == 'down' else False
                        sise = stock_rate[0].select('span.sise')
                        i['sise'] = sise[0].text.strip()
                        rate = stock_rate[0].select('span.rate')
                        i['rate'] = rate[0].text.strip()
                    else:
                        i['invalid'] = True
                else:
                    i['invalid'] = True
            except:
                i['invalid'] = True

        d = get('http://finance.daum.net/item/main.daum?code={code}'.format(code=code))
        d.addCallback(lambda v: v.text()).addCallback(on_complete, stock)

        return d

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def stock_get_all(self, request):
        yield self.stock_init()
        r = [{'stockName': item['stockName'], 'stockCode': k} for k, item in self.stock_master.items()]

        question = request.args.get('question', [''])[0]
        if question:
            r = [i for i in r if question in i['stockName']]
        total_length = len(r)

        if request.args.get('sortBy'):
            r.sort(key=lambda v: v['stockName'])

        page = int(request.args['page'][0])
        rows_per_page = int(request.args['rowsPerPage'][0])
        r = r[(page - 1) * rows_per_page:page * rows_per_page]

        dlist = []
        for i in r:
            d = self.stock_sise(i, i['stockCode'][1:])
            dlist.append(d)
            d = self.stock_per(i, i['stockCode'][1:])
            dlist.append(d)
            d = self.stock_eps(i, i['stockCode'][1:])
            dlist.append(d)

        r = yield defer.DeferredList(dlist).addCallback(
                lambda v: json.dumps({'stocks': r, 'totalLength': total_length}))
        defer.returnValue(r)

    @refine_twisted_web_request
    @defer.inlineCallbacks
    def stock_get(self, request, code):
        r = yield get('http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code[1:]))
        r = yield r.text()
        data = []
        soup = BeautifulSoup(r, 'html.parser')
        items = soup.find_all('tr', {'onmouseover': 'mouseOver(this)'})
        for i, _ in enumerate(items):
            e = {'date': items[i].find_all('td', {'align': 'center'})[0].text}
            m = items[i].find_all('td', {'class': 'num'})
            e['curPrice'] = m[0].text.strip()
            img = m[1].find_all('img')
            if img:
                e['down'] = True if img[0]['alt'] == '하락' else False
            e['sise'] = m[1].text.strip()
            e['volume'] = m[5].text.strip()
            data.append(e)

        defer.returnValue(json.dumps(data))


def add_stocks_routes(app):
    s = Stock()
    app.route('/api/stocks', methods=['GET'])(s.stock_get_all)
    app.route('/api/stocks/<string:code>', methods=['GET'])(s.stock_get)
