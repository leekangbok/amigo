import random
import sqlite3

from bs4 import BeautifulSoup
from requests import get

from backend.webscrapy.stock.stock_code import stocks


def per_of_fiveyears_serv(code):
    response = get('http://search.itooza.com/search.htm?seName={}'.format(code))
    soup = BeautifulSoup(response.text, 'html.parser')

    r = soup.select('p.table-desc')
    r = r[0].select('strong')

    s = soup.select('div.item-data1')
    s = s[0].select('tr td')

    t = soup.select('div.item-data2')
    t = t[0].select('tr td')

    return r[0].string.strip(), t[0].string.strip(), t[1].string.strip(), s[0].string.strip(), s[1].string.strip()


if __name__ == '__main__':
    conn = sqlite3.connect('../../../data.db')
    cur = conn.cursor()

    for stock in stocks:
        try:
            x = per_of_fiveyears_serv(stock['stock_code'][1:])
            # print(stock['stock_code'][1:], x)
            cur.execute(
                'insert into StockPerPbr (uid,reg_date,mod_date,stock_code,'
                'last_date,five_years_per,five_years_pbr,last_per,last_pbr) '
                'values (?,?,?,?,?,?,?,?,?)', (str(random.randint(1000000, 9000000)), 0, 0, stock['stock_code'], *x))
        except Exception as e:
            print(e)
            print('error', stock['stock_code'][1:])

    conn.commit()
    conn.close()
