#! /usr/bin/python
# encoding:utf-8

import requests
import json
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

    vip_url = ["http://www.qicycling.cn/category/report",
               "http://www.qicycling.cn/category/deep"]

    with requests.Session() as s:
        login()
        # for article_id in list:
        #     if check_article_in_app(cursor_app, article_id) == True:
        #         break
        #
        #     vip_url = "http://www.qicycling.cn/%d.html"%article_id
        #     response = s.get(vip_url)
        #
        #     href_html = response.text
        #     html, img_list, author, video_list, title = sync.get_href_detail(href_html)
        #     print html
        #     break

        article_id = int(sys.argv[1])
        print type(article_id)
        print(article_id)
        vip_url = "http://www.qicycling.cn/%d.html" % article_id
        response = s.get(vip_url)
        href_html = response.text
        html, img_list, author, video_list, title = sync.get_href_detail(href_html)
        html_n = html.replace('私密：', '')
        title = title.replace('私密：', '')
        h5 = sync.save_h5(html_n, article_id)
        description = title
        t = time.time()
        ts = int(round(t * 1000))

        # 修改title
        cursor_app.execute("SELECT id from resource where id=%d" % article_id)
        result = cursor_app.fetchone()
        if result is None:
            sql = "INSERT INTO resource (id, title, description, status, h5url, is_vip, publisher, type,TIMESTAMP)" \
                " VALUES (%d, '%s', '%s', 1, '%s', 1, '%s', 0, %d)" % (
                article_id, title, description, h5, author, ts)
        else:
            sql = "UPDATE resource set title='%s', description='%s', is_vip=1 where id=%d" % (title, title, article_id)

        #print sql
        cursor_app.execute(sql)

        cursor_app.execute("DELETE FROM resource_image where resource_id=%d" % article_id)
        for i in xrange(len(img_list)):
            img = img_list[i]
            # surl = quote(img['url'])
            surl = img['url']
            sql = "INSERT INTO resource_image (resource_id, height, `length`, url) values (%d,%d,%d,'%s')" % (
                article_id, int(img['width']), int(img['height']), surl)
            cursor_app.execute(sql)

        cursor_app.execute("DELETE FROM module_resource where resource_id=%d" % article_id)
        sync.add_resource_module(cursor_wp, cursor_app, article_id)

        #print html

    db_app.commit()
    db_wp.commit()