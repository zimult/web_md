# -*- coding: utf-8 -*-

#import logging
#from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
#import db
import requests
import time
from flask import request, redirect
import urllib, urllib2
import json
import sys
from ali.alipay import *
from util.tools import *
from xmly_sign import get_sign

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


def get_trade_no():
    return "123456"


@shorty_api.route('/ali_order', methods=['GET', 'POST'])
def ali_order():
    #state = request.values.get('state')
    alipay = AliPay(
        appid="2018052160236073",
        app_notify_url="http://projectsedus.com/",
        app_private_key_path="ali/app_private_key_2048.txt",
        alipay_public_key_path="ali/alipay_public_key_sha256.txt",
        # alipay_public_key_path="./app_public_key_2048.txt",
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,
        return_url=""
    )
    out_trade_no = get_trade_no()
    subject = request.values.get('subject')
    total_fee = request.values.get('total_fee')
    item_desc = request.values.get('item_desc')
    data = {}
    data['partner']='2018052160236073'
    data['service'] = 'mobile.securitypay.pay'
    data['_input_charset'] = 'UTF-8'
    data['sign_type'] = 'RSA'
    data['notify_url'] = 'https://app.yuan7dan.com/alipay/notify'
    data['app_id'] = 'app_id'
    data['out_trade_no'] = out_trade_no
    data['subject'] = subject
    data['payment_type'] = '1'
    data['seller_id'] = '2088421398130544'
    data['total_fee'] = str(total_fee)
    data['body'] = item_desc


    print type(data)

    sign_str, sign_s = alipay.sign_data(data)

    return sign_s


@shorty_api.route('/test_xmly', methods=['GET', 'POST'])
def test_xmly():
    return "test ok! xmly"


@shorty_api.route('/all_paid_albums', methods=['GET', 'POST'])
def all_paid_albums():
    url = "https://api.ximalaya.com/open_pay/all_paid_albums"
    ts = int(round(time.time() * 1000))
    params = {
        'page':1,
        'count':20,
        'app_key':'b617866c20482d133d5de66fceb37da3',
        'client_os_type':4,
        'nonce':'a3878a1a361229e0a34eb9931d229e69',
        'timestamp':ts
    }
    sign = get_sign(params)
    params['sig'] = sign
    print params
    res = requests.get(url, params)
    print res.status_code, res.text

    return res.text





if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8000 )
