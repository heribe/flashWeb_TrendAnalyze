#coding:utf-8
import requests

# user_info = {'name': 'letian', 'password': '123'}
# r = requests.post("http://127.0.0.1:5000/xmlin", data=user_info)
#
# print(r.text)

xml = """<data>
    <fun>1</fun>
    <num>3</num>
    <items>
        <item>1539,1540,1541,1542,1543,1544,1545,1546,1547,1548,1549,1550</item>
        <item>3087,4555,7815,9705,4700,4703,5252,4709,4712,1705,4718,4721</item>
        <item>3421,4199,3612,3569,3525,3459,3405,3347,3229,1208,4187,4155</item>
    </items>
</data>"""
headers = {'Content-Type':'application/xml'} # set what your server accepts
print requests.post('http://127.0.0.1:5000/xmlin', data=xml, headers=headers).text