# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
# import db
import requests
import time
from flask import request, redirect
import urllib, urllib2
import json
import sys
from ali.alipay import *
from util.tools import *
from xmly_sign import *  # get_sign, get_public_param

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf8')

appKey = 'f9aee5687ff7d8e66cdeff6a3c63c81a'
appSecret = '4fd4c41d4fe59a183ffd106a61d895bc'

formatter = logging.Formatter('%(asctime)s %(levelname)s [%(thread)d] %(message)s')  # 每行日志的前缀设置
log = logging.getLogger('werkzeug')
fileTimeHandler = TimedRotatingFileHandler('./log/' + 'xmly.log', "d", 1, 30)
# 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix 如果需要更改需要改logging 源码
fileTimeHandler.suffix = "%Y%m%d"
logging.basicConfig(level=logging.INFO)
fileTimeHandler.setFormatter(formatter)
log.addHandler(fileTimeHandler)

shorty_api = Flask(__name__)

log.info("------ server start.")


# db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
# db_app = db.DB(config.host, config.user, config.password, config.database_app)


def access_token2(code, device_id):
    # url = "http://192.168.3.54:8206/oauth2-auth-app/v2/access_token"
    url = "https://api.ximalaya.com/oauth2/v2/access_token"

    headers = {"Content-type": "application/x-www-form-urlencoded"}
    body = {'grant_type': 'authorization_code',
            'redirect_uri': 'https://app.yuan7dan.com/redirect_uri',
            'client_secret': appSecret,
            'client_id': appKey,
            'device_id': device_id,
            'code': code,
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


def xmly_refresh_token(device_id, r_token):
    url = "https://api.ximalaya.com/oauth2/refresh_token"
    body = {'grant_type': 'refresh_token',
            # 'redirect_uri': 'http://api.test.ximalaya.com:8137/openapi-collector-app/get_access_token',
            'redirect_uri': 'https://app.yuan7dan.com/redirect_uri',
            'client_secret': appSecret,
            'client_id': appKey,
            'device_id': device_id,
            'refresh_token': r_token,
            }
    r = requests.post(url, body)
    print r.text
    return r.text


@shorty_api.route('/redirect_uri', methods=['GET', 'POST'])
def redirect_uri():
    code = request.values.get('code')
    state = request.values.get('state')
    device_id = request.values.get('device_id')
    # print id
    log.info("redirect_uri device_id:{}".format(device_id))
    rt = access_token(code, device_id)
    log.info("redirect_uri access_token return:{}".format(rt))
    rt_j = json.loads(rt)
    if rt_j.has_key('error_no'):
        return rt
    return rt
    # if rt_j.has_key('refresh_token'):
    #     rf_token = rt_j['refresh_token']
    #     dv_id = rt_j['device_id']
    #     log.info("redirect_uri - to refresh_token:{}, device_id:{}".format(rf_token, dv_id))
    #     rt2 = xmly_refresh_token(dv_id, rf_token)
    #     log.info("redirect_uri - refresh_token return:{}".format(rt2))
    #     js2 = json.loads(rt2)
    #     if js2.has_key('error_no'):
    #         log.error("error: refresh_token return [%s]" % rt2)
    #     else:
    #         rt_j['access_token'] = js2['access_token']
    #         rt_j['refresh_token'] = js2['refresh_token']
    #         rt_j['expires_in'] = js2['expires_in']
    # # print("redirect_url return:{}"%js)
    # # return json.dumps(js)
    # log.info("redirect_uri return:{}".format(rt_j))
    # return json.dumps(rt_j)


@shorty_api.route('/refresh_token', methods=['GET', 'POST'])
def refresh_token():
    try:
        log.info(request.headers)
        device_id = request.values.get('device_id')
        rf_token = request.values.get('refresh_token')
        log.info(request.get_data())
        log.info(request.get_json())
        log.info("refresh_token request:{}".format(request.values))
        log.info("refresh_token device_id:{}, refresh_token={}".format(device_id, rf_token))
        rt = xmly_refresh_token(device_id, rf_token)
        log.info("refresh_token return:{}".format(rt))
        rt_j = json.loads(rt)
        if rt_j.has_key('error_no'):
            return rt
        return rt
    except:
        return "参数格式错误"


def get_trade_no():
    return "123456"


@shorty_api.route('/ali_order', methods=['GET', 'POST'])
def ali_order():
    # state = request.values.get('state')
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
    data['partner'] = '2018052160236073'
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
        'page': 1,
        'count': 20,
        'app_key': 'b617866c20482d133d5de66fceb37da3',
        'client_os_type': 4,
        'nonce': 'a3878a1a361229e0a34eb9931d229e69',
        'timestamp': ts
    }
    sign = get_sign(params)
    params['sig'] = sign
    print params
    res = requests.get(url, params)
    print res.status_code, res.text

    return res.text


@shorty_api.route('/xmly', methods=['GET', 'POST'])
def xmly():
    params = {}
    for k, v in request.values.items():
        params[k] = v
    log.info(params)
    req_api = params['req_api']
    params.pop('req_api')
    public_param = get_public_param()

    params.update(public_param)

    print request.method
    sig = get_sign(params)
    params['sig'] = sig
    log.info(params)

    #url = "https://api.ximalaya.com" + req_api
    url = "https://mpay.ximalaya.com" + req_api

    if request.method == 'GET':
        res = requests.get(url, params)
    else:
        res = requests.post(url, params)
    print res.status_code, res.text
    return res.text


# 下单
@shorty_api.route('/open_pay/place_order', methods=['GET', 'POST'])
def place_order():
    params = {}
    log.info("/open_pay/place_order params recv:{}".format(request.values))
    for k, v in request.values.items():
        log.info("k:{}, v:{}".format(k,v))
        params[k] = v
    log.info("/open_pay/place_order params recv:{}".format(params))
    # 记录本方数据库 订单表

    device_id = request.values.get('device_id')
    #params.pop('device_id')
    public_param = get_public_param()
    params.update(public_param)

    sig = get_sign(params)
    params['sig'] = sig
    log.info("/open_pay/place_order params send:{}".format(params))
    url = "https://api.ximalaya.com" + '/open_pay/place_order'

    # if request.method == 'GET':
    #     res = requests.get(url, params)
    # else:
    res = requests.post(url, params)
    log.info("xmly return code:{}, info:{}".format(res.status_code, res.text))
    rsp = json.loads(res.text)
    if rsp.has_key('error_no'):
        # 有错误
        error_no = rsp['error_no']
    else:
        xima_order_no = rsp['xima_order_no']
        xima_order_status = rsp['xima_order_status']
        xima_order_created_at = rsp['xima_order_created_at']
        xima_order_updated_at = rsp['xima_order_updated_at']
        # 更新数据库
    return res.text


# 确认订单
@shorty_api.route('/open_pay/confirm_order', methods=['POST', 'GET'])
def confirm_order():
    dt = dict(request.args)
    params = {}
    for k, v in dt.items():
        params[k] = v[0]
    req_api = request.path

    device_id = request.values.get('device_id')
    params.pop('device_id')
    public_param = get_public_param()
    params.extend(public_param)

    print params
    print request.method
    sig = get_sign(params)
    params['sig'] = sig
    url = "https://api.ximalaya.com" + req_api

    if request.method == 'GET':
        res = requests.get(url, params)
    else:
        res = requests.post(url, params)
    print res.status_code, res.text
    res = json.loads(res.text)
    if res.has_key('error_no'):
        # 有错误
        error_no = res['error_no']
    else:
        xima_order_no = res['xima_order_no']
        xima_order_status = res['xima_order_status']
        xima_order_created_at = res['xima_order_created_at']
        xima_order_updated_at = res['xima_order_updated_at']
        # 更新数据库
    return res.text

@shorty_api.route('/open_pay/get_price_info', methods=['POST', 'GET'])
def get_price_info():
    sq = ""
#

if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8000)
