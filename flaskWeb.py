
# -*- coding: utf8 -*-
from flask import Flask, request
from flask import Response


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/xmlin',methods=['POST'])
def xmlin():
    print ("************SERVER CALLED ***********")
    print request.data
    xml = """<?xml version='1.0' encoding='utf-8'?>
<a>7</a>"""
    return Response(xml, mimetype='application/xml')


if __name__ == '__main__':
    app.run()
