#coding:utf-8
import requests

# user_info = {'name': 'letian', 'password': '123'}
# r = requests.post("http://127.0.0.1:5000/xmlin", data=user_info)
#
# print(r.text)

xml = """<?xml version='1.0' encoding='utf-8'?>
<a>б</a>"""
headers = {'Content-Type':'application/xml'} # set what your server accepts
print requests.post('http://localhost:5000/xmlin', data=xml, headers=headers).text