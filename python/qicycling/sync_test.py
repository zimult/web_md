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
import chardet

import traceback
from fn import log, db_app, db_wp
from urllib import quote
from urllib import unquote
import sync

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == '__main__':
    # page = 0
    # while (True):
    #     page += 1
    #     articles = sync.getArticle(page)
    #     print articles
    #     break

    # html, img_list, author, video_list = sync.get_href('http://www.qicycling.cn/4213.html')
    # print html

    i= 52
    j = 5

    tmp = 1
    for m in xrange(1,i):
        tmp = m * tmp
    print tmp
