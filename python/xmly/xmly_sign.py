# -*- coding: utf-8 -*-
__author__ = 'zimult'

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256, HMAC, SHA
from base64 import b64encode, b64decode
from urllib import quote_plus
from urlparse import urlparse, parse_qs
from urllib import urlopen
import base64
import json
import hmac
import hashlib
from util.tools import *
import sys
import time
import jpush
from enum import Enum

reload(sys)
sys.setdefaultencoding('utf-8')

#A_key = 'b617866c20482d133d5de66fceb37da3'
#A_secret = '4d8e605fa7ed546c4bcb33dee1381179'
#serverAuthenticateStaticKey = 'z0hh5l9A'

A_key = 'f9aee5687ff7d8e66cdeff6a3c63c81a'
A_secret = '4fd4c41d4fe59a183ffd106a61d895bc'
serverAuthenticateStaticKey = 'ptx0LdPn'

jpush_app_key = ""
jpush_secret = ""


class ConfirmType(Enum):
    pay = 1  # 支付
    cancle = 2  # 取消或失败


class OrderStatus(Enum):
    pay = 1  # 等待支付
    success = 2  # 支付成功
    cancle = 3  # 支付失败


def get_public_param():
    param = {}
    param['app_key'] = A_key
    param['nonce'] = rand_string(8)
    param['client_os_type'] = 1
    param['timestamp'] = int(round(time.time() * 1000))
    # param['sig'] = ''
    return param


def ordered_data(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据dump出来
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))
    return sorted([(k, v) for k, v in data.items()])


def get_sign2(data):
    unsigned_items = ordered_data(data)
    # for k, v in unsigned_items:
    #     print k,v
    # unsigned_string = "&".join("{0}={1}".format(k, lib.unicode_2_str(v)) for k, v in unsigned_items)
    unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
    print unsigned_string
    b64_str = base64.b64encode(unsigned_string.encode('utf-8'))
    # sha1Key = A_secret + serverAuthenticateStaticKey
    print b64_str
    print "YWNjZXNzX3Rva2VuPTc1ZGJlYzdmMWZjMjg5MTQ1YTg4NjkwMzA3NzU3ZjlkJmFwcF9rZXk9YjYxNzg2Nm" \
          "MyMDQ4MmQxMzNkNWRlNjZmY2ViMzdkYTMmY2xpZW50X29zX3R5cGU9MiZkZXZpY2VfaWQ9MDhkODMzZjU4" \
          "MjZlOHdrJnBhY2tfaWQ9Y29tLmFwcC50ZXN0LmFuZHJvaWQmcT3ogarmmI7kuI7mmbrmhac="
    # sha1Key = '4d8e605fa7ed546c4bcb33dee1381179de5kio2f'
    sha1Key = '4d8e605fa7ed546c4bcb33dee1381179z0hh5l9A'

    # hmac.new(Token, data, hashlib.sha1).digest().encode('base64').rstrip()
    r1 = hmac.new(sha1Key, b64_str, hashlib.sha1).digest()  # .encode('base64')#.hexdigest()#.encode('base64').rstrip()
    r2 = hmac.new(sha1Key, b64_str, hashlib.sha1).hexdigest()

    l = []
    for i in xrange(len(r1)):
        t = ord(r1[i])
        if t < 0:
            t = t + 256
            print t
        l.append(t)
    print l

    print r2
    print r1.encode('base64').rstrip()
    print len(r1), len(r2), type(r1)
    print str_md5(bytearray(r1))
    print str_md5(bytearray(l))
    print str_md5(r1.encode('base64').rstrip())
    print str_md5(r2), type(r2)


def get_sign(data):
    unsigned_items = ordered_data(data)
    # for k, v in unsigned_items:
    #     print k,v
    # unsigned_string = "&".join("{0}={1}".format(k, lib.unicode_2_str(v)) for k, v in unsigned_items)
    unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
    print unsigned_string
    b64_str = base64.b64encode(unsigned_string.encode('utf-8'))
    print b64_str
    # sha1Key = A_secret
    sha1Key = A_secret + serverAuthenticateStaticKey
    #sha1Key = serverAuthenticateStaticKey + A_secret
    # sha1Key = A_secret + 'de5kio2f'
    #sha1Key = 'de5kio2f'

    # hmac.new(Token, data, hashlib.sha1).digest().encode('base64').rstrip()
    # h = hmac.new(bytearray(sha1Key), bytearray(unsigned_string), SHA)
    h = hmac.new(sha1Key, b64_str, hashlib.sha1)
    r = h.digest()
    # print r, len(r)
    sign = str_md5(r)
    # print sign.rstrip()
    # print str_md5(bytearray(r))
    return sign.rstrip()

def get_sign_log(log, data):
    unsigned_items = ordered_data(data)
    # for k, v in unsigned_items:
    #     print k,v
    # unsigned_string = "&".join("{0}={1}".format(k, lib.unicode_2_str(v)) for k, v in unsigned_items)
    unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
    log.info("unsigned_string:{}".format(unsigned_string))
    b64_str = base64.b64encode(unsigned_string.encode('utf-8'))
    log.info("b64_str:{}".format(b64_str))
    # sha1Key = A_secret
    sha1Key = A_secret + serverAuthenticateStaticKey
    #sha1Key = serverAuthenticateStaticKey + A_secret
    # sha1Key = A_secret + 'de5kio2f'
    #sha1Key = 'de5kio2f'
    log.info("sha1Key:{}".format(sha1Key))
    # hmac.new(Token, data, hashlib.sha1).digest().encode('base64').rstrip()
    # h = hmac.new(bytearray(sha1Key), bytearray(unsigned_string), SHA)
    h = hmac.new(sha1Key, b64_str, hashlib.sha1)
    r = h.digest()
    # print r, len(r)
    sign = str_md5(r)
    # print sign.rstrip()
    # print str_md5(bytearray(r))
    return sign.rstrip()


def test():
    str = "access_token=75dbec7f1fc289145a88690307757f9d&app_key=b617866c20482d133d5de66fceb37da3&client_os_type=2&device_id=08d833f5826e8wk&pack_id=com.app.test.android&q=聪明与智慧"
    b64_x = 'YWNjZXNzX3Rva2VuPTc1ZGJlYzdmMWZjMjg5MTQ1YTg4NjkwMzA3NzU3ZjlkJmFwcF9rZXk9YjYxNzg2NmMyMDQ4MmQxMzNkNWRlNjZmY2ViMzdkYTMmY2xpZW50X29zX3R5cGU9MiZkZXZpY2VfaWQ9MDhkODMzZjU4MjZlOHdrJnBhY2tfaWQ9Y29tLmFwcC50ZXN0LmFuZHJvaWQmcT3ogarmmI7kuI7mmbrmhac='
    b64_m = base64.b64encode(str, 'utf-8')
    if b64_x == b64_m:
        print "same base64"
    else:
        print "diff base64"
    # print b64_m
    # print b64_x
    sha1Key = '4d8e605fa7ed546c4bcb33dee1381179de5kio2f'
    r1 = hmac.new(sha1Key, b64_x, hashlib.sha1).digest()
    r3 = hmac.new(sha1Key, b64_x, hashlib.sha1)._current()

    print r3, type(r3)
    r2 = bytearray(r1)
    r = [46, -33, -13, 57, -109, 79, 49, 31, -45, -128, -3, 75, -127, -23, -102, 37, -101, -110, -12, -43]
    print len(r1), len(r)
    for i in xrange(len(r)):
        if r[i] < 0:
            r[i] = r[i] + 256
    lst = []
    lst2 = []
    for elem in r1:
        # print elem
        lst.append(elem)
        lst2.append(ord(elem))
    print r
    print lst
    print lst2

    print str_md5(bytearray(r))
    print str_md5(r1)
    print str_md5(r1.encode('base64').rstrip())
    print str_md5(bytearray(r1))
    print str_md5(bytearray(r2))


def test2():
    # url = "https://api.ximalaya.com/categories/list?access_token=77eca96155c50179141549792edb7570&app_key=b617866c20482d133d5de66fceb37da3&client_os_type=2&device_id=df529d6e9b56c15b&pack_id=com.ushaqi.zhuishushenqi&sig=332853e55f696a7e8926bc5235ee31ff"
    url = "https://mpay.ximalaya.com/openapi-payfacade-app/open_pay/place_order?" \
          "app_key=b617866c20482d133d5de66fceb37da3&device_id=123456789&client_os_type=1&nonce=6509976" \
          "d0894817e2ad4452b69ee74fa&timestamp=1498716218179&third_uid=20170324&price_type=" \
          "1&pay_content=19586586&price=9.90"

    # url = "https://mpay.ximalaya.com/openapi-payfacade-app/open_pay/confirm_order?app_key=b617866c20482d133d5de66fceb37da3&device_id=123456789&client_os_type=1&nonce=1" \
    #       "309976d0894817e2ad4452b69ee74fa&timestamp=1498716218809&third_uid=20170324&xima_order_" \
    #       "no=20170324001712240000000023649378&pay_channel=2&confirm_type=1&sig=c543ea1bfacab9f772b28f1253619673"

    # url = "https://mpay.ximalaya.com/openapi-payfacade-app/open_pay/get_order_detail?" \
    #       "app_key=b617866c20482d133d5de66fceb37da3&device_id=123456789&client_os_type=1&third_ui" \
    #       "d=20170324&nonce=6509976" \
    #       "d0894817e2ad4452b69ee74fa&timestamp= 498716218179&xima_order_n" \
    #       "o=20170324001712240000000023649378&sig=ebb8d87e8c73500126ba14f997f95d3a"

    o = urlparse(url)
    query = parse_qs(o.query)
    processed_query = {}
    if query.has_key('sig'):
        sig = query.pop("sig")[0]
        # sig = "ebb8d87e8c73500126ba14f997f95d3a"
        # a = ""
    else:
        sig = "c543ea1bfacab9f772b28f1253619673"

    for key, value in query.items():
        processed_query[key] = value[0]
    # print type(processed_query)
    print processed_query
    sign = get_sign(processed_query)

    print "---------- {} == {} : {}".format(sig, sign, sig == sign)
    # print get_sign2(processed_query)
    # print "----------"


if __name__ == '__main__':
    test2()


    # l = ['{:02X}'.format(ord(i)) for i in r]
    # s = ''.join(l)
    # news = bytearray.fromhex(s)
    # print "s=", s
    # print "news=", news
