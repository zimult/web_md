#! /usr/bin/python
# encoding:utf-8

import requests
import json
import time
import config
import db
import os
import datetime
import sys

import traceback
from fn import log, db_app, db_wp
from urllib import quote
from urllib import unquote

reload(sys)
sys.setdefaultencoding('utf8')

'''
Google Trend 热词
热词的访问次数是有限制的，现在暂时不知道限制有多少，建议每天更新一次，因为数据的分辨率是以day来记录的，所以每天更新一次不会对结果造成多大影响
https://bikeridejoy.herokuapp.com/api/trend/index/<symbol>/<months>
返回json格式，key为timestamp，以毫秒记，先除以1000后再转化datetime，value为热词指数
<months>为1-3，由于google trend api限制只能搜3个月以内的
<symbol>为自行车品牌.docx 中的任一自行车品牌，全小写
其中三个只有中文没有英文的品牌对应英文如下
‘feige’:’飞鸽’,
‘phoenix’:’凤凰’,
‘forever’:’永久’,
'''

brand_list = [
    ['Giant', '捷安特'],
    ['Merida', '美利达'],
    ['TREK', '崔克'],
    ['Specialized', '闪电'],
    ['BMC'],
    ['LOOK', '路克'],
    ['SRAM', '速联'],
    ['shimano', '禧玛诺'],
    ['cannondale', '佳能戴尔'],
    ['Pinarello', '皮纳瑞罗'],
    ['Kuota'],
    ['SCOTT', '斯科特'],
    ['Cervelo'],
    ['UCC'],
    ['KUNG', '攻队'],
    ['FOCUS'],
    ['missile', '米赛尔'],
    ['ORBEA', '欧贝亚'],
    ['JAVA', '佳沃'],
    ['De Rosa'],
    ['Colnago', '梅花'],
    ['Kona'],
    ['Schwinn', '施文'],
    ['Bianchi', '比安奇'],
    ['Gusto', '高士特'],
    ['Cinelli'],
    ['Fuji', '富士'],
    ['BH'],
    ['WILIER', '威廉'],
    ['飞鸽'],
    ['凤凰自行车'],
    ['Cube'],
    ['永久'],
    ['ZGL'],
    ['XDS', '喜德盛'],
    ['TIME', '自行车'],
    ['Canyon'],
    ['LAPIERRE', '拉皮尔'],
    ['凯路仕'],
    ['3T'],
    ['Factor'],
    ['Argon18'],
    ['Ridley'],
    ['pardus', '瑞豹'],
    ['Campagnolo'],
    ['Power2Max'],
    ['SRM'],
    ['Rotor'],
    ['Moots'],
    ['Olympia'],
    ['ENVE'],
    ['OYAMA', '欧亚马'],
    ['YETI'],
    ['LiteSpeed'],
    ['Lightweight'],
    ['FSA'],
    ['QUICK'],
    ['Taokas', '道卡斯'],
    ['KTM'],
    ['Author'],
    ['NeilPryde'],
    ['Ceepo', '袭豹'],
    ['CAMP', '坎普'],
    ['TRINX', '千里达'],
    ['Triace', '骓驰'],
    ['intense'],
    ['Tropix', '烈风'],
    ['GALAXY', '格莱仕'],
    ['Santa Cruz'],
    ['NORCO', '诺客']
]


def import_brand(cursor):
    t = time.time()
    ts = int(round(t * 1000))

    for i in xrange(len(brand_list)):
        brand_name = brand_list[i][0]
        brand_name_cn = ''
        if len(brand_list[i]) > 1:
            brand_name_cn = brand_list[i][1]

        print brand_name, brand_name_cn
        cursor.execute("INSERT INTO brand (status,`name`,name_cn,`TIMESTAMP`) values (1,'%s','%s',%d)"
                       % (brand_name, brand_name_cn, ts))


def get_brand_list(cursor):
    list = []
    cursor.execute("SELECT id, `name`, name_cn FROM brand where status=1 and type=0")
    result = cursor.fetchall()
    for row in result:
        list.append(row)
    return list


def get_google_trend(cursor, list):
    for row in list:
        brand_id, brand_name, brand_name_cn = row
        check_name = brand_name.lower()

        get_google_trend_brand(cursor, check_name, brand_id)


def get_google_trend_brand(cursor, check_name, brand_id):
    # print brand_id, brand_name, brand_name_cn

    if check_name == '飞鸽':
        check_name = 'feige'
    elif check_name == '凤凰':
        check_name = 'phoenix'
    elif check_name == '永久':
        check_name = 'forever'

    # url = "https://bikeridejoy.herokuapp.com/api/trend/index/"+check_name+"/3"
    url = "https://bikeridejoy.herokuapp.com/api/trend/index/" + check_name
    print url
    try:
        res = requests.get(url)
        print res.text
        js = json.loads(res.text)
    except Exception, e:
        print(e.message)
        print(traceback.format_exc())
        return

    t = time.time()
    ts = int(round(t * 1000))

    # print js
    # for key in js:
    #     rt = js[key]
    #     for tk in rt:
    #         tm = int(tk)/1000
    #         num = int(rt[tk])
    #         time_l = time.localtime(tm)
    #         insert_brand_opinion(cursor, brand_id, time_l, num, ts)
    item = js[0]
    for k, v in item.items():
        print k, v
        ts = int(round(t * 1000))
        insert_brand_opinion(cursor, brand_id, v, 1, ts)


def insert_brand_opinion(cursor, brand_id, value, num, ts):
    #str_time = datetime.now().strftime("%Y-%m-%d") + "08:00:00"
    str_time = time.strftime("%Y-%m-%d", time.localtime()) + " 08:00:00"
    cursor.execute("SELECT id FROM brand_opinion where `day`='%s' and brand_id=%d" % (str_time, brand_id))
    result = cursor.fetchone()
    if result is None:
        sql = "INSERT INTO brand_opinion (`day`,full_num,num,brand_id,`timestamp`)" \
              " VALUES ('%s',%d,1,%d,%d)" % (str_time, value, brand_id, ts)
        # print sql
        cursor.execute(sql)
    else:
        id = result[0]
        # print id
        cursor.execute("UPDATE brand_opinion set full_num=%d, `timestamp`=%d where id=%d" % (value, ts, id))


if __name__ == '__main__':
    # s = ''
    # html, img_list, author, video_list = sync.get_href('http://www.qicycling.cn/2927.html')
    # print html

    # print time.time()
    # cursor_wp = db_wp.get_cursor()
    cursor_app = db_app.get_cursor()

    # import_brand(cursor_app)
    # db_app.commit()
    b_l = get_brand_list(cursor_app)
    print b_l

    get_google_trend(cursor_app, b_l)
    #
    # get_google_trend_brand(cursor_app, '3T')
    db_app.commit()
