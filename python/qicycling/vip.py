#! /usr/bin/python
# encoding:utf-8

import requests
import json
import time
from bs4 import BeautifulSoup
from bs4 import NavigableString
import config
import db
import os
from PIL import Image
import sys
import cStringIO, urllib2
import time
import sync

import traceback
from fn import log, db_app, db_wp
from urllib import quote
from urllib import unquote

reload(sys)
sys.setdefaultencoding('utf8')

def login():
    print "正在请求登录页面..."
    login_page_url = "http://www.qicycling.cn/wp-login.php"
    login_html = s.get(login_page_url)
    print "正在解析"
    #post_key = get_post_key(login_html.text)

    login_url = "http://www.qicycling.cn/wp-login.php"
    #name, password = get_account()
    login_data = s.post(url=login_url, data={
        "log": 'guyyu',
        "pwd": 'guyyxd118'
    })
    print login_data.text


if __name__ == '__main__':
    # banner
    with requests.Session() as s:
        login()

        vip_url = "http://www.qicycling.cn/1158.html"
        response = s.get(vip_url)


        #html, img_list, author, video_list = sync.get_href(vip_url)
        print response.text

