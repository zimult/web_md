# encoding:utf-8

import requests
import json
import time
import datetime
from bs4 import BeautifulSoup
from bs4 import NavigableString
import config
import db
import os
from PIL import Image
import sys
import cStringIO, urllib2
import time
import chardet

import traceback
from fn import log, db_app, db_wp
from urllib import quote
from urllib import unquote
import sync

reload(sys)
sys.setdefaultencoding('utf8')

import time, datetime

def now_milliseconds():
   return int(time.time() * 1000)

# reference time.time
# Return the current time in seconds since the Epoch.
# Fractions of a second may be present if the system clock provides them.
# Note: if your system clock provides fractions of a second you can end up
# with results like: 1405821684785.2
# our conversion to an int prevents this

def date_time_milliseconds(date_time_obj):
   return int(time.mktime(date_time_obj.timetuple()) * 1000)

# reference: time.mktime() will
# Convert a time tuple in local time to seconds since the Epoch.


if __name__ == '__main__':
    # page = 0
    # while (True):
    #     page += 1
    #     articles = sync.getArticle(page)
    #     print articles
    #     break

    # html, img_list, author, video_list, title = sync.get_href('http://www.qicycling.cn/4919.html')
    # print title
    #print html

    ts = 736856
    print datetime.fromtimestamp(ts)
