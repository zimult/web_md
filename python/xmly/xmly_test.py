import requests
import json
import sys
from xmly_sign import *


def get_price_info():
    url = "https://mpay.ximalaya.com" + "/open_pay/get_price_info"
    params = {"album_id": '4345263', 'client_os_type':'1', 'third_uid':'20170331', 'device_id':'123456789'}
    public_param = get_public_param()
    params.update(public_param)

    # succ
    # params = {'nonce': '6509976d0894817e2ad4452b69ee74fa', 'album_id': '4345263', 'third_uid': '20170331',
    #  'app_key': 'b617866c20482d133d5de66fceb37da3', 'client_os_type': '1',
    #  'timestamp': int(round(time.time() * 1000)), 'device_id': '123456789'}

    sig = get_sign(params)
    params['sig'] = sig
    print params
    res = requests.get(url, params)
    print res.status_code, res.text


def test_sing():
    url = "https://mpay.ximalaya.com/openapi-payfacade-app/open_pay/get_price_info?" \
          "app_key=b617866c20482d133d5de66fceb37da3&device_id=123456789&client_os_type=1&third_ui" \
          "d=20170331&nonce=6509976d0894817e2ad4452b69ee74fa&timestamp=1498716218179&album_id=434" \
          "5263&sig=7e5e85a0116373d6dedc77919268dc50"
    o = urlparse(url)
    query = parse_qs(o.query)
    processed_query = {}
    if query.has_key('sig'):
        sig = query.pop("sig")[0]
    else:
        sig = "7e5e85a0116373d6dedc77919268dc50"
    print sig
    for key, value in query.items():
        processed_query[key] = value[0]
    # print type(processed_query)
    processed_query['timestamp'] = int(round(time.time() * 1000))
    sig = get_sign(processed_query)
    processed_query['sig'] = sig
    print processed_query

    url = "https://mpay.ximalaya.com" + "/open_pay/get_price_info"
    res = requests.get(url, processed_query)
    print res.text

if __name__ == '__main__':
    get_price_info()

    #test_sing()
