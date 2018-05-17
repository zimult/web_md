# -*- coding: utf-8 -*-

#import logging
#from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
import db
from flask import request
import sync
from mresponse import *
import traceback

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
        url = "http://www.qicycling.cn/%d.html"%article_id
        html, img_list, author, v_list, title = sync.get_href(url)
        h5 = sync.save_h5(html, article_id)

        # 修改title
        # sql = "INSERT INTO resource (id, title, description, status, h5url, is_vip, publisher, type,TIMESTAMP)" \
        #       " VALUES (%d, '%s', '%s', 1, '%s', 0, '%s', 0, %d)" % (
        #       article_id, title, description, h5, author, ts * 1000)
        cursor_app.execute("UPDATE source set title='%s', description='%s' where id=%d"%(title, title, article_id))

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
        rt = {'code': 1, 'result':article_id, 'error':''}
        return fmt_response(rt)
    except Exception, e:
        db_app.rollback()
        db_wp.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')

if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8410 )
