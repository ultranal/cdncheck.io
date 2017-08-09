#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json, request

app = Flask(__name__)

@app.route("/", methods=['POST'])
def json0():
    return json.loads(request.get_data())['hostname']

    
if __name__ == '__main__':
    app.run(debug=True)