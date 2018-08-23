#coding:utf-8
import requests

# user_info = {'name': 'letian', 'password': '123'}
# r = requests.post("http://127.0.0.1:5000/xmlin", data=user_info)
#
# print(r.text)

xml = """<data>
    <fun>1</fun>
    <num>2</num>
    <items>
        <item>1538,1681,1961,1741,1448,1748,1784,2036,1732,1182,1797,1744</item>
        <item>1784,2036,1732,1182,1797,1744,1538,1681,1961,1741,1448,1748</item>
    </items>
</data>"""
headers = {'Content-Type':'application/xml'} # set what your server accepts
print requests.post('http://localhost:5000/xmlin', data=xml, headers=headers).text