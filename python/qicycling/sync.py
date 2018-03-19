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

import traceback
from fn import log, db_app

def getBanner(pageUrl):
    try:
        list = []

        # read from url
        response = requests.get(pageUrl)
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        banner = soup.select('[class="item"]')
        for i in xrange(len(banner)):
            # print type(banner[i])
            tag = banner[i]
            banner_url = tag.get('style')[22:-2]

            x = 0
            chan = ''
            text = ''
            for child in tag.stripped_strings:
                if x == 0:
                    chan = child
                if x == 1:
                    text = child
                x += 1

            #print("banner:" + banner_url + ", chan:" + chan + ", text:" + text)
            rt = {'banner':banner_url, 'chan': chan, 'text':text}
            list.append(rt)
        return list
    except Exception, e:
        print e


def recordBanner(db_app, banners):
    cursor = db_app.get_cursor()
    try:
        for banner in banners:
            url = banner['banner']
            text = banner['text']

            cursor.execute("SELECT id FROM banner where pic_url='%s' and title='%s'"%(url, text))
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO banner (pic_url, title, create_date, update_date, `position`, `resource_type`) values ('%s', '%s', now(), now(), 'index', 1)"%(url, text)
                print sql
                cursor.execute(sql)
            else:
                print "banner exists..."
                pass
            db_app.commit()
    except Exception, e:
        log.error(e.message)
        log.error(traceback.format_exc())

def getArticle(page):
    # curl -d 'paged=0&action=ajax_load_posts&append=home-list&page=home' http://www.qicycling.cn/wp-admin/admin-ajax.php
    url = "http://www.qicycling.cn/wp-admin/admin-ajax.php"

    list = []

    data = {'paged': page, 'action': 'ajax_load_posts', 'append': 'list', 'page': 'home'}
    r = requests.post(url, data)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    #articles = soup.select('[class="image"]')
    articles = soup.select('article')
    for article in articles:
        #print article

        images = article.select('[class="image"]')
        image = images[0]
        #print image
        img = image.select('img')

        if len(img) <= 0:
            continue

        a1 = img[0].attrs
        a2 = image.select('a')[0].attrs
        a1.update(a2)

        contents = article.select('[class="content"]')
        chans = contents[0].select('a')
        a1['chan'] = chans[0].text
        a1['text'] = chans[1].text

        href = a1['href']
        article_id = os.path.basename(href).split('.')[0]
        a1['article_id'] = article_id

        #print a1
        list.append(a1)

        ### debug break
        #break

    return list


def get_href(url):
    # "Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
    # headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36'}
    # response = requests.get(url, headers)
    #print url

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    html_head = soup.head.prettify()
    html_top = '' + html_head
    # print html_head

    ######## no data
    # new_html = html_top + '\n' \
    #                       "<body class=\"post-template-default single single-post single-format-standard\">\n" \
    #                       "<section class=\"nt-warp nt-warp-nospace\">\n" \
    #                       "<div class=\"container\">\n" \
    #                       "<div class=\"suxing post-cover\">\n"
    #
    # cover = soup.findAll('div', {'class': 'suxing post-cover'})
    # # for i in xrange(len(cover)):
    # #     html_article = cover[i]
    # for cv in cover:
    #     #print html_article
    #     #print cv
    #     h2 = cv.find('div', {'class': 'image'})
    #     #print h2.prettify()
    #     new_html += h2.prettify()
    #
    #     h1 = cv.find('h1')
    #     #print h1
    #     new_html += h1.prettify()
    #
    #     author = cv.find('div', {'class': 'author-name'})
    #     #print author
    #     new_html += author.prettify()
    #     aname = author.find('a').text
    #
    # new_html = new_html + '\n</div>\n'
    ##################### no data

    #####################  data
    new_html = html_top + '\n' \
                          "<body class=\"post-template-default single single-post single-format-standard\">\n" \
                          "<section class=\"nt-warp nt-warp-nospace\">\n" \
                          "<div class=\"container\">\n"

    cover = soup.findAll('div', {'class': 'suxing post-cover'})
    for i in xrange(len(cover)):
        html_article = cover[i].prettify()
        new_html += html_article

    add_str = "<div class =\"row\">" \
                          "<main class =\"l-main col-xs-12 col-sm-8 col-md-9\">" \
                          "<div class =\"m-post\">"
    new_html += add_str

    article = soup.select('article')
    for i in xrange(len(article)):
        html_article = article[i].prettify()
        # print html_article
        new_html += html_article

    new_html = new_html + '</div>\n</main>\n</div>\n' + '</div>\n</section>\n</body>'

    author = soup.find('div', {'class': 'author-name'})
    author_name = ''
    if author:
        author_name = author.find('a').text

    # img_list
    img_list = []

    # post-image
    #srcsets = soup.findAll('div', {'class': 'post-image'})
    srcsets = soup.select('article')
    for srcset in srcsets:
        imgs = srcset.findAll('img')
        if len(imgs)<=0:
            continue
        for img in imgs:
            img_url = img.get('src')
            width = img.get('width')
            height = img.get('height')
            if width is None or height is None:
                print img_url
                img_ = Image.open(requests.get(img_url, stream=True).raw)
                width, height = img_.size

            pinfo = {'url':img_url, 'width':int(width), 'height':int(height)}
            img_list.append(pinfo)

    return new_html, img_list, author_name


def recordArticle(db_app, articles):
    cursor = db_app.get_cursor()
    try:
        for article in articles:
            article_id = article['article_id']
            img_url = article['src']
            title = article['alt']
            description = article['text']
            href = article['href']
            html, img_list, author = get_href(href)

            # 时间从 db_wp 读取 wp_posts.id =
            if len(img_list) <= 0:
                img_list.append(img_url)
            print article_id, img_list, author, title, description

        db_app.commit()
    except Exception, e:
        log.error(e.message)
        log.error(traceback.format_exc())

# url = "http://www.qicycling.cn"
# getBanner(url)
#
# list = getArticle()
#
# for info in list:
#     src = info['src']
#     href = info['href']
#     alt = info['alt']
#     get_href(href)
#     print alt

if __name__ == '__main__':
    # banner

    # banners = getBanner(config.web_url)
    # recordBanner(db_app, banners)

    articles = getArticle(1)
    recordArticle(db_app, articles)

    #print  getArticle(2)

    # 1377
    # 1370 post-template-default single single-post postid-1370 single-format-standard logged-in admin-bar no-customize-support
    # 1363 post-template-default single single-post postid-1363 single-format-standard logged-in admin-bar no-customize-support post-style03
    # 1365

    ## 1346
    ## 1329
    # html, img_list, author = get_href('http://www.qicycling.cn/1370.html')
    # print img_list
    # print author

