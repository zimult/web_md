# -*- coding: utf-8 -*-

#import logging
#from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
#import db
import requests
from flask import request, redirect
import urllib, urllib2
import json
import sys

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf8')

shorty_api = Flask(__name__)

# db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
# db_app = db.DB(config.host, config.user, config.password, config.database_app)
appKey = 'f9aee5687ff7d8e66cdeff6a3c63c81a'
appSecret = '4fd4c41d4fe59a183ffd106a61d895bc'

def access_token2(code, device_id):
    #url = "http://192.168.3.54:8206/oauth2-auth-app/v2/access_token"
    url = "https://api.ximalaya.com/oauth2/v2/access_token"

    headers = {"Content-type": "application/x-www-form-urlencoded"}
    body = {'grant_type':'authorization_code',
            'redirect_uri':'https://app.yuan7dan.com/redirect_uri',
            'client_secret':appSecret,
            'client_id':appKey,
            'device_id':device_id,
            'code':code,
            }
    print body
    test_data_urlencode = urllib.urlencode(body)
    request = urllib2.Request(url=url, headers=headers, data=test_data_urlencode)
    rt = urllib2.urlopen(request).read()
    print rt

def access_token(code, device_id):
    url = "https://api.ximalaya.com/oauth2/v2/access_token"
    body = {'grant_type': 'authorization_code',
            'redirect_uri': 'https://app.yuan7dan.com/redirect_uri',
            'client_secret': appSecret,
            'client_id': appKey,
            'device_id': device_id,
            'code': code,
            }
    print body
    r = requests.post(url, body)
    print r.text
    return r.text

def refresh_token(device_id, refresh_token):
    url = "https://api.ximalaya.com/oauth2/refresh_token"
    body = {'grant_type': 'refresh_token',
            #'redirect_uri': 'http://api.test.ximalaya.com:8137/openapi-collector-app/get_access_token',
            'redirect_uri': 'https://app.yuan7dan.com/redirect_uri',
            'client_secret': appSecret,
            'client_id': appKey,
            'device_id': device_id,
            'refresh_token': refresh_token,
            }
    r = requests.post(url, body)
    print r.text
    return r.text

@shorty_api.route('/redirect_uri', methods=['GET', 'POST'])
def redirect_uri():
    code = request.values.get('code')
    state = request.values.get('state')
    device_id = request.values.get('device_id')
    #print id

    rt = access_token(code, device_id)
    rt_j = json.loads(rt)
    if rt_j.has_key('error_no'):
        return rt


    # if rt_j.has_key('refresh_token'):
    #     rf_token = rt_j['refresh_token']
    #     print(rf_token)
    #     rt2 = refresh_token(device_id, rf_token)
    #     js = json.loads(rt2)
    #     if js.has_key('error_no'):
    #         print("refresh_token return [%s]"%rt2)
    #         return rt2

    print rt
    return rt

    #return "haah"

@shorty_api.route('/test_xmly', methods=['GET', 'POST'])
def test_xmly():
    return "test ok! xmly"

if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8000 )
