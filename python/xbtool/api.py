# -*- coding: utf-8 -*-

import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
import db
import requests
import time
from flask import request, redirect
import urllib, urllib2
import json
import traceback
import sys

from response import *

requests.packages.urllib3.disable_warnings()
reload(sys)
sys.setdefaultencoding('utf8')

formatter = logging.Formatter('%(asctime)s %(levelname)s [%(thread)d] %(message)s')  # 每行日志的前缀设置
log = logging.getLogger('werkzeug')
fileTimeHandler = TimedRotatingFileHandler('./log/' + 'xb.log', "d", 1, 30)
# 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix 如果需要更改需要改logging 源码
fileTimeHandler.suffix = "%Y%m%d"
logging.basicConfig(level=logging.INFO)
fileTimeHandler.setFormatter(formatter)
log.addHandler(fileTimeHandler)

shorty_api = Flask(__name__)

log.info("------ server start.")

mysql_db = db.DB(config.host, config.user, config.password, config.database)


# db_app = db.DB(config.host, config.user, config.password, config.database_app)
@shorty_api.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    cursor = mysql_db.get_cursor()
    count = request.values.get('count')

    try:
        # 从db获取id
        sql = "INSERT INTO "
        self.cursor.execute(sql)
        id = int(self.cursor.lastrowid)

        piclist = []
        for i in xrange(count):
            filek = "file_" + str(i + 1)

            f = request.files[filek]
            filename = f.filename
            extendname = os.path.splitext(filename)[1]
            key = rand.randfilename() + extendname
            dictorypath = config.upload_path
            if not os.path.exists(dictorypath):
                os.mkdir(dictorypath)
            upload_path = os.path.join(dictorypath, key)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
            f.save(upload_path)
            # upload_key = 'news/' + key
            # result = qn.upload_file(upload_key, upload_path)
            ##os.remove(upload_path)
            ##if result.status_code == 200:
            ##return my_response(upload_key)
            store_url = config.server_addr + key;

            # insert db (id, i+1, store_url, time)
            piclist.append(store_url)
        mysql_db.commit()
        return my_response(piclist)
    except Exception, e:
        pic_mysql_db.rollback()
        mysql_db.rollback()
        log.error(e.message)
        log.error(traceback.format_exc())
        return my_response_error(300, '处理失败')


@shorty_api.route('/list_file', methods=['GET', 'POST'])
def list_file():
    cursor = mysql_db.get_cursor()
    try:
        id = request.values.get('id')
        list = []
        sql = "SELECT pid, store_url From xx WHERE id={}".format(id)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            pid, url = row[0]
            tmp = {"pid": pid, "url": url}
            list.append(tmp)
        mysql_db.commit()
        return my_response(list)
    except Exception, e:
        pic_mysql_db.rollback()
        mysql_db.rollback()
        log.error(e.message)
        log.error(traceback.format_exc())
        return my_response_error(300, '处理失败')


if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=81000)
