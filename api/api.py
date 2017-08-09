#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, Response, make_response
import json
import cdncheck
import domaincheck
app = Flask(__name__)

@app.route("/api/ip/lookup", methods=['POST', 'OPTIONS'])
def iplookup():
    if request.method == 'OPTIONS':
        rst = make_response("")
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'POST'
        rst.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type' 
        return rst, 201
    ret = json.loads(request.get_data())
    ret = cdncheck.iplookup(
        ret['hostname'],
        ret['iprange'],
        ret['spec'],
        ret['onlySuccFlag']
    )
    rst = make_response(jsonify(ret))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst, 201


@app.route("/api/domain/lookup", methods=['POST', 'OPTIONS'])
def domainlookup():
    if request.method == 'OPTIONS':
        rst = make_response("")
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'POST'
        rst.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type' 
        return rst, 201
    ret = json.loads(request.get_data())
    ret = domaincheck.domainlookup(
        ret['url'],
        ret['domainList'],
        ret['spec'],
        ret['onlySuccFlag']
    )
    rst = make_response(jsonify(ret))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst, 201
    
if __name__ == "__main__":
	app.run(debug=True)