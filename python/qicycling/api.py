# -*- coding: utf-8 -*-

# import logging
# from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
import db
from flask import request
import sync
from mresponse import *
import traceback
import time
import os

shorty_api = Flask(__name__)

db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
db_app = db.DB(config.host, config.user, config.password, config.database_app)


@shorty_api.route('/sync_article', methods=['GET', 'POST', 'OPTIONS'])
def sync_article():
    try:
        article_id = int(request.values.get('article_id'))

        # 删除文章,等待重新同步
        cursor_app = db_app.get_cursor()
        cursor_wp = db_wp.get_cursor()

        # cursor.execute("DELETE FROM resource where id=%d"%article_id)
        # cursor.execute("DELETE FROM resource_image where resource_id=%d"%article_id)
        # cursor.execute("DELETE FROM module_resource where resource_id=%d"%article_id)
        url = "http://www.qicycling.cn/%d.html" % article_id
        html, img_list, author, v_list, title = sync.get_href(url)
        h5 = sync.save_h5(html, article_id)

        # 修改title
        # sql = "INSERT INTO resource (id, title, description, status, h5url, is_vip, publisher, type,TIMESTAMP)" \
        #       " VALUES (%d, '%s', '%s', 1, '%s', 0, '%s', 0, %d)" % (
        #       article_id, title, description, h5, author, ts * 1000)
        sql = "UPDATE resource set title='%s', description='%s' where id=%d" % (title, title, article_id)
        print sql
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

        db_app.commit()
        db_wp.commit()
        rt = {'code': 1, 'result': article_id}
        return fmt_response(rt)
    except Exception, e:
        db_app.rollback()
        db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/add_match', methods=['GET', 'POST', 'OPTIONS'])
def add_match():
    try:
        #
        title = request.values.get('title')
        date = request.values.get('date') + " 00:00:00"
        city = request.values.get('city')

        sd = ''
        if request.values.has_key('sd'):
            sd = request.values.get('sd')
        gc = ''
        if request.values.has_key('gc'):
            gc = request.values.get('gc')
        url = ''
        if request.values.has_key('url'):
            url = request.values.get('url')
        live_url = ''
        if request.values.has_key('live_url'):
            live_url = request.values.get('live_url')

        id = None
        cursor_app = db_app.get_cursor()

        if request.values.has_key('id'):
            id = int(request.values.get('id'))
            sql = "UPDATE schedule set `date`='{}',title='{}',rackinger='{}'," \
                  "url='{}',area='{}',leg='{}',live_url='{}' WHERE id={}".format(date, title, gc, url, city, sd,
                                                                                 live_url, id)
        else:
            # 增加数据
            t = time.time()
            ts = int(round(t * 1000))
            if len(url) > 0:
                sql = "INSERT INTO schedule (status,`date`,title,`timestamp`,rackinger,url,area,leg,live_url)" \
                      " VALUES (1,'%s','%s',%d,'%s','%s','%s','%s', '%s')" % (
                          date, title, ts, gc, url, city, sd, live_url)
            else:
                sql = "INSERT INTO schedule (status,`date`,title,`timestamp`,rackinger,area,leg,live_url)" \
                      " VALUES (1,'%s','%s',%d,'%s','%s','%s', '%s')" % (date, title, ts, gc, city, sd, live_url)
        print sql
        cursor_app.execute(sql)
        db_app.commit()
        # db_wp.commit()

        return fmt_response('success')
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/list_match', methods=['GET', 'POST', 'OPTIONS'])
def list_match():
    try:
        st = request.values.get('st')
        et = request.values.get('et')
        cursor_app = db_app.get_cursor()

        sql = "SELECT id,`date`,title,ifnull(rackinger,''),ifnull(url,''),ifnull(area,''),ifnull(leg,''), ifnull(live_url,'') FROM schedule" \
              " WHERE `date` between '%s 00:00:00' and '%s 23:59:59'" % (st, et)
        print sql
        cursor_app.execute(sql)
        result = cursor_app.fetchall()
        list = []
        for row in result:
            print row
            id, dt, title, rackinger, url, area, leg, live_url = row
            tmp = {'id': id, 'date': dt.split(' ')[0], 'title': title, 'rackinger': rackinger, 'url': url, 'area': area,
                   'leg': leg, 'live_url': live_url}
            list.append(tmp)

        db_app.commit()
        print list
        return fmt_response(list)
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/get_match', methods=['GET', 'POST', 'OPTIONS'])
def get_match():
    try:
        id = int(request.values.get('id'))
        cursor_app = db_app.get_cursor()

        sql = "SELECT id,`date`,title,ifnull(rackinger,''),ifnull(url,''),ifnull(area,''),ifnull(leg,''), ifnull(live_url,'') FROM schedule" \
              " WHERE id={}".format(id)
        print sql
        cursor_app.execute(sql)
        result = cursor_app.fetchone()

        id, dt, title, rackinger, url, area, leg, live_url = result
        tmp = {'id': id, 'date': dt.split(' ')[0], 'title': title, 'rackinger': rackinger, 'url': url, 'area': area,
               'leg': leg, 'live_url': url}
        db_app.commit()
        return fmt_response(tmp)
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/del_match', methods=['GET', 'POST', 'OPTIONS'])
def del_match():
    try:
        id = int(request.values.get('id'))
        cursor_app = db_app.get_cursor()
        cursor_app.execute("DELETE FROM schedule where id=%d" % id)

        db_app.commit()
        return fmt_response("success")
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')

        db_app.commit()
        print list
        return fmt_response(list)


@shorty_api.route('/sync_vip', methods=['GET', 'POST', 'OPTIONS'])
def sync_vip():
    try:
        article_id = int(request.values.get('article_id'))
        cursor_app = db_app.get_cursor()
        cursor_wp = db_wp.get_cursor()

        # check if article_id is vip
        sql = "SELECT * from wp_posts where `id`=%d and post_type='post' and post_status='private'" % article_id
        print sql
        cursor_wp.execute(sql)
        result = cursor_wp.fetchone()
        if result is None:
            return fmt_response_error(501, '不是VIP文章类型')

        cmd = "/var/www/traveler/qyc/vip.sh %d" % article_id
        os.system(cmd)
        db_app.commit()
        db_wp.commit()
        return fmt_response("success")
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/delete_article', methods=['POST'])
def delete_article():
    try:
        article_id = int(request.values.get('article_id'))
        cursor_app = db_app.get_cursor()
        cursor_wp = db_wp.get_cursor()
        cursor_app.execute("delete from resource_banner where resource_id =%d" % article_id)
        cursor_app.execute("delete from resource_image where resource_id =%d" % article_id)
        cursor_app.execute("delete from module_resource where resource_id =%d" % article_id)
        cursor_app.execute("delete from resource_praise where resource_id =%d" % article_id)
        cursor_app.execute("delete from resource_collection where resource_id =%d" % article_id)
        cursor_app.execute("delete from resource where id =%d" % article_id)
        db_app.commit()
        db_wp.commit()
        return fmt_response("success")
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/list_module', methods=['GET', 'POST'])
def list_module():
    try:
        cursor_app = db_app.get_cursor()
        cursor_app.execute("select id, status, `name` from `module` where parent_id = 1")
        result = cursor_app.fetchall()
        list = []
        for row in result:
            id, status, name = row
            tmp = {'id': id, 'status': status, 'name': name}
            list.append(tmp)
        db_app.commit()
        return fmt_response(list)
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


@shorty_api.route('/update_module_main', methods=['GET', 'POST'])
def update_module_main():
    try:
        cursor_app = db_app.get_cursor()
        lst = request.values.get('list')
        # print lst
        # print type(lst)
        arr = json.loads(lst)
        str = ','.join(arr)
        print str
        cursor_app.execute("UPDATE `module` set status=0 where parent_id=1")
        cursor_app.execute("UPDATE `module` set status=1 where parent_id=1 and id in ({})".format(str))
        db_app.commit()
        return fmt_response("success")
    except Exception, e:
        db_app.rollback()
        # db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')


if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8410)
