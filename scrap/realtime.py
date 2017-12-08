from requests import get
from bs4 import BeautifulSoup

url = 'http://finance.naver.com/item/main.nhn?code=010140'
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rate_info = soup.select('#chart_area > div.rate_info')
today_sise = rate_info[0].select('div p.no_today')
print(today_sise[0].select('span.blind')[0].string)

# print(rate_info[0].select('div p.no_exday'))
today_sise = rate_info[0].select('div p.no_exday em.no_down')
for i in today_sise:
    print(i.find('span', attrs={"class": "ico"}))
    # p = i.previous_sibling
    # print(p.string)