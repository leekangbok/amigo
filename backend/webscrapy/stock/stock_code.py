import json

from requests import get

url = 'http://www.financipe.com/api/stockmaster'


def stock_code_serve():
    response = get(url)
    return json.loads(response.text)


stocks = stock_code_serve()

if __name__ == '__main__':
    stock_code_serve()
