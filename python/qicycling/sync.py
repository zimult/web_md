#! /usr/bin/python
# encoding:utf-8

import requests
import json
import time
from bs4 import BeautifulSoup
from bs4 import NavigableString


def getBanner(pageUrl):
    try:
        time.sleep(1)

        # read from url
        response = requests.get(pageUrl)
        html = response.text

        # read file
        # hfile = open('qy.html', 'r')
        # html = hfile.read()

        soup = BeautifulSoup(html, "html.parser")
        # banner = soup.find_all("div", 'container-fluid pd0')
        # print(type(banner))
        # print banner.children


        # banner = soup.find_all("div", re.compile("item$"))
        # banner = soup.find_all(attrs={"class":"item"})
        # print len(banner)
        # for i in xrange(len(banner)):
        #     print banner[i]

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

            print("banner:" + banner_url + ", chan:" + chan + ", text:" + text)
            print "-------------- cnt:" + str(i)

    except Exception, e:
        print e
    finally:
        pass


def getArticle():
    # curl -d 'paged=0&action=ajax_load_posts&append=home-list&page=home' http://www.qicycling.cn/wp-admin/admin-ajax.php
    url = "http://www.qicycling.cn/wp-admin/admin-ajax.php"

    list = []

    page = 1
    data = {'paged': page, 'action': 'ajax_load_posts', 'append': 'list', 'page': 'home'}
    r = requests.post(url, data)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select('[class="image"]')
    for i in xrange(len(article)):
        print article[i]

        idx = 0
        temp = {}
        for child in article[i].descendants:
            idx += 1
            if idx == 2:
                temp = child.attrs
            if idx == 4:
                temp.update(child.attrs)
        list.append(temp)
        print "-------------- article cnt:" + str(i)

    return list


def get_href(url):
    # "Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36"
    # headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; OD103 Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36'}
    # response = requests.get(url, headers)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # print soup.html
    # print soup.head.prettify()

    # print soup.body.prettify()
    # return soup.html

    html_head = soup.head.prettify()
    html_top = '' + html_head
    # print html_head

    # article = soup.select('suxing post-cover')
    new_html = html_top + '\n' \
                          "<body class=\"post-template-default single single-post single-format-standard\">\n" \
                          "<section class=\"nt-warp nt-warp-nospace\">\n" \
                          "<div class=\"container\">\n"

    cover = soup.findAll('div', {'class': 'suxing post-cover'})
    for i in xrange(len(cover)):
        html_article = cover[i].prettify()
        new_html += html_article

    new_html = new_html + "<div class =\"row\">" \
                          "<main class =\"l-main col-xs-12 col-sm-8 col-md-9\">" \
                          "<div class =\"m-post\">"

    article = soup.select('article')
    for i in xrange(len(article)):
        html_article = article[i].prettify()
        # print html_article
        new_html += html_article

    new_html = new_html + '</div>\n</main>\n</div>\n' + '</div>\n</section>\n</body>'

    # img_list
    srcsets = soup.findAll('div', {'class': 'wp-caption alignnone'})
    # print srcsets
    img_list = []
    for srcset in srcsets:
        img = srcset.find('img')
        img_url = img.get('src')
        img_list.append(img_url)

    return new_html, img_list


def get_top_html():
    file = open('top.html', 'r');
    html_top = file.read()
    file.close

    return html_top


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


html, img_list = get_href('http://www.qicycling.cn/1307.html')
print html
