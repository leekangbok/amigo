import json

import requests

data = {
    'uid'     : '',
    'mod_date': 0,
    'author'  : 'haram',
    'subject' : '테스트 글',
    'body'    : '블라블라 안녕하세요.',
    'clicked' : 100
}
res = requests.post("http://localhost:5000/api/doctor/consulting", data=json.dumps(data))
print(res.text)

params = {'subject': '테스트'}
res = requests.get("http://localhost:5000/api/doctor/consulting", params=params)
print(res.text)

res = requests.get('http://localhost:5000/api/doctor/consulting/{}'.format('3d4b621d15d74975'))
print(res.text)


data = {
    'author'  : 'haram',
    'subject' : '고친글 글',
    'body'    : '고친글입니다.',
    'clicked' : 200
}
res = requests.put('http://localhost:5000/api/doctor/consulting/{}'.format('3d4b621d15d74975'), data=json.dumps(data))
print(res.text)


data = {
    'body': '댓글',
    'consulting_uid': '995b78ae040359a9'
}
res = requests.post('http://localhost:5000/api/doctor/consulting_reply', data=json.dumps(data))
print(res.text)

params = {'uid': '995b78ae040359a9'}
res = requests.get("http://localhost:5000/api/doctor/consulting", params=params)
print(res.text)