# -*- coding: utf-8 -*-

import json
from flask import make_response
import datetime

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def fmt_response(data):
    result = {'code': 1, 'result': data, 'error': ''}
    #return json.dumps(result, ensure_ascii=False, cls=CJsonEncoder)
    res = make_response(json.dumps(result, ensure_ascii=False, cls=CJsonEncoder))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

def fmt_response_error(code, error, result=None):
    if result == None:
        result = { 'code':code, 'result':'', 'error':error}
    else:
        result = { 'code':code, 'result':result, 'error':error}

    res = make_response( json.dumps(result, ensure_ascii=False, cls=CJsonEncoder) )
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res