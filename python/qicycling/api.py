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
        cursor = db_app.get_cursor()

        cursor.execute("DELETE FROM resource where id=%d"%article_id)
        cursor.execute("DELETE FROM resource_image where resource_id=%d"%article_id)
        cursor.execute("DELETE FROM module_resource where resource_id=%d"%article_id)

        db_app.commit()
        rt = {'code': 1, 'result':article_id, 'error':''}
        return fmt_response(rt)
    except Exception, e:
        db_app.rollback()
        print(e.message)
        print(traceback.format_exc())
        return fmt_response_error(0, '处理失败')



if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8410 )
