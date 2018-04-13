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
    # login_page_url = "http://www.qicycling.cn/wp-login.php"
    # login_html = s.get(login_page_url)
    # print "正在解析"
    #post_key = get_post_key(login_html.text)

    login_url = "http://www.qicycling.cn/wp-login.php"
    #name, password = get_account()
    login_data = s.post(url=login_url, data={
        "log": 'guyyu',
        "pwd": 'guyyxd118'
    })
    #print login_data.text

def get_private_article(cursor):
    list = []
    cursor.execute("SELECT `id`, TIMESTAMPDIFF(DAY, post_date, now()) from wp_posts where post_type='post' and post_status='private' order by id desc")
    result = cursor.fetchall()
    for row in result:
        id, days = row
        list.append(id)
    return list

def check_article_in_app(cursor, article_id):
    cursor.execute("SELECT id FROM resource where id=%d"%article_id)
    result = cursor.fetchone()
    if result is None:
        return False
    return True

if __name__ == '__main__':
    # s = ''
    # html, img_list, author, video_list = sync.get_href('http://www.qicycling.cn/2927.html')
    # print html

    cursor_wp = db_wp.get_cursor()
    cursor_app = db_app.get_cursor()
    list = get_private_article(cursor_wp)

    with requests.Session() as s:
        login()

        for article_id in list:
            if check_article_in_app(cursor_app, article_id) == True:
                break

            vip_url = "http://www.qicycling.cn/%d.html"%article_id
            response = s.get(vip_url)

            href_html = response.text
            html, img_list, author, video_list = sync.get_href_detail(href_html)
            print html
            break

