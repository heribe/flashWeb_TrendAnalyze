#coding:utf-8
import requests

# user_info = {'name': 'letian', 'password': '123'}
# r = requests.post("http://127.0.0.1:5000/xmlin", data=user_info)
#
# print(r.text)

xml = """<data>
    <fun>2</fun>
    <num>5</num>
    <items>
        <item>1538,1681,1961,1741,1448,1748,1784,2036,1732,1182,1797,1744</item>
        <item>600,601,400,603,345,605,606,567,608,643,610,611</item>
        <item>400,478,893,403,343,405,406,407,408,19,410,411</item>
        <item>169,189,202,232,256,205,266,555,208,11,267,211</item>
        <item>369,413,466,503,504,533,506,507,508,509,510,511</item>
    </items>
</data>"""
headers = {'Content-Type':'application/xml'} # set what your server accepts
print requests.post('http://54.95.66.128:5000/xmlin', data=xml, headers=headers).text