
# -*- coding: utf8 -*-
from flask import Flask, request
from flask import Response
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/xmlin',methods=['POST'])
def xmlin():
    print ("************SERVER CALLED ***********")
    print request.data
    xml = request.data
    return Response(xml, mimetype='application/xml')


if __name__ == '__main__':
    app.run()
