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

reload(sys)
sys.setdefaultencoding('utf8')

def downloadPic(url):
    basename = os.path.basename(url)
    #print basename
    cmd = "curl " + url + " -o pic/" + basename
    os.system(cmd)
    return "pic/" + basename

def getPicSize(file):
    img_ = Image.open(file)
    width, height = img_.size
    return width, height

def getUrlPicSize(url):
    file = downloadPic(url)
    img_ = Image.open(file)
    width, height = img_.size
    #os.remove(file)
    return width, height

def getBanner(pageUrl):
    try:
        list = []

        # read from url
        response = requests.get(pageUrl)

        html = response.text
        #print html

        soup = BeautifulSoup(html, "html.parser")
        ca = soup.find('div', {'class': 'container-fluid pd0'})
        #print ca

        # banner = ca.select('[class="item"]')
        # for i in xrange(len(banner)):
        #     # print type(banner[i])
        #     tag = banner[i]
        #     banner_url = tag.get('style')[22:-2]
        #
        #     x = 0
        #     chan = ''
        #     text = ''
        #     for child in tag.stripped_strings:
        #         if x == 0:
        #             chan = child
        #         if x == 1:
        #             text = child
        #         x += 1
        #
        #     #print("banner:" + banner_url + ", chan:" + chan + ", text:" + text)
        #     rt = {'banner':banner_url, 'chan': chan, 'text':text}
        #     list.append(rt)

        banners = ca.findAll('a', {'class': 'permalink'})
        for banner in banners:
            #print banner
            href = banner.attrs['href']
            base = os.path.basename(href).split('.')[0]
            #print base
            list.append(base)

        return list
    except Exception, e:
        print e
        print traceback.format_exc()

def recordBanner_pic(db_app, banners):
    cursor = db_app.get_cursor()
    try:
        for banner in banners:
            url = banner['banner']
            text = banner['text']

            cursor.execute("SELECT id FROM banner where pic_url='%s' and title='%s'"%(url, text))
            result = cursor.fetchone()
            if result is None:
                t = time.time()
                ts = int(round(t * 1000))
                sql = "INSERT INTO banner (pic_url, title, `timestamp`, `position`, `resource_type`) values ('%s', '%s', %d, 'index', 1)"%(url, text, ts)
                #print sql
                cursor.execute(sql)
            else:
                print "banner exists..."

            db_app.commit()
    except Exception, e:
        log.error(e.message)
        log.error(traceback.format_exc())

def recordBanner(db_app, banners):
    cursor = db_app.get_cursor()
    try:
        modules = get_modules(db_app)
        str = ','.join(banners)
        #print str
        cursor.execute("DELETE FROM resource_banner where resource_id not in (%s)"%str)

        for bn in banners:
            banner = int(bn)
            for module in modules:
                cursor.execute("SELECT id FROM resource_banner where `position`=%d and resource_id=%d"%(module, banner))
                result = cursor.fetchone()
                if result is None:
                    t = time.time()
                    ts = int(round(t * 1000))
                    cursor.execute("INSERT INTO resource_banner (status, `timestamp`, `position`, resource_id) values (1, %d,%d,%d)"%(ts,module,banner))
                else:
                    print "banner exists ..."

        db_app.commit()
    except Exception, e:
        log.error(e.message)
        log.error(traceback.format_exc())


def get_modules(db_app):
    list = []
    cursor = db_app.get_cursor()
    cursor.execute("SELECT id FROM `module` WHERE parent_id = 1")
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        #print id
        list.append(id)
    return list

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
            print images[0]
            print("--------- not found img")
            continue

        a1 = img[0].attrs
        a2 = image.select('a')[0].attrs
        a1.update(a2)

        contents = article.select('[class="content"]')
        chans = contents[0].select('a')
	#print chans[0].text
        a1['chan'] = ''
        if len(chans) == 2:
            print chans[1].text
            a1['chan'] = chans[0].text
            a1['text'] = chans[1].text
        else:
            a1['text'] = chans[0].text

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
    # print url

    response = requests.get(url)
    html = response.text
    return get_href_detail(html)

def get_href_detail(html):
    soup = BeautifulSoup(html, "html.parser")
    #print type(soup)
    soup.find('div', {'class': 'post-footer clearfix'}).extract()

    utime = soup.findAll('span', {'class': 'u-time'})
    len_utime = len(utime)
    print len_utime
    for i in range(0, len_utime):
        soup.find('span', {'class': 'u-time'}).extract()
    #print soup.prettify()
    #print soup

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
                          "<body class=\"post-template-default single single-post single-format-standard\">\n"

    ##// 视频文件
    video_list = []
    videos = soup.findAll('section', {'class': 'nt-warp nt-warp-video pt0'})
    if len(videos) > 0:
        for i in xrange(len(videos)):
            html_article = videos[i].prettify()
            new_html += html_article

            vs = videos[i].select('iframe')
            for v in vs:
                print v.attrs['src']
                video_list.append(v.attrs['src'])
    ## 普通文章
    else:
        new_html += "<section class=\"nt-warp nt-warp-nospace\">\n" \
                    "<div class=\"container\">\n"
        cover = soup.findAll('div', {'class': 'suxing post-cover'})
        print("cover len:%d"%len(cover))
        for i in xrange(len(cover)):
            html_article = cover[i].prettify()
            new_html += html_article

        add_str = "<div class =\"row\">" \
                  "<main class =\"l-main col-xs-12 col-sm-8 col-md-9\">" \
                  "<div class =\"m-post\">"
        new_html += add_str

        article = soup.select('article')
        #print("article len:%d" % len(article))
        for i in xrange(len(article)):
            html_article = article[i].prettify()
            # print html_article
            new_html += html_article

        # 加上作者信息
        # author-info
        if new_html.find("author-info") == -1:
            author_info = soup.find('div', {'class': 'post-author clearfix'})
            if author_info:
                new_html += author_info.prettify()

        new_html = new_html + '</div>\n</main>\n</div>\n' + '</div>\n</section>\n'

    new_html += "</body>"

    #footer = soup.find('div', {'class': 'post-footer clearfix'})
    #footer_text = footer.prettify()
    #print footer_text

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
                try:
                    img_ = Image.open(requests.get(img_url, stream=True).raw)
                    width, height = img_.size
                except Exception, e:
                    try:
                        width, height = getUrlPicSize(img_url)
                    except Exception, e:
                        log.error(e.message)
                        log.error(traceback.format_exc())
                        continue

            pinfo = {'url':img_url, 'width':int(width), 'height':int(height)}
            if(int(width) > 100):
                img_list.append(pinfo)

    new_html = new_html.replace("src=\"//v.qq.com", "src=\"https://v.qq.com")

    '''
    idx1 = new_html.find('<a class="btn-action btn-like')
    print idx1
    # idx1 = new_html.find('<div class="post-footer clearfix">')
    # #print idx1
    h1 = new_html[0:idx1]
    h2 = new_html[idx1:]

    # idx_f = new_html.find(footer_text)
    # print idx_f
    # print len(footer_text)
    #
    idx2 = h2.find("</a>")
    # # str2 = "下载封面\n</a>\n</p>\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>\n</div>"
    # # idx2 = h2.find(str2)
    # # print idx2
    #h3 = h2[idx2+len(str2):]
    h3 = h2[idx2+4:]
    # # ＃h3 = "下载封面"
#
    nh = h1 + h3
    '''

    #print new_html
    #print nh
    return new_html, img_list, author_name, video_list

def save_h5(html, article_id):
    filename = config.html_path + str(article_id) + '.html'
    #filename = "./_" + str(article_id) + '.html'
    with open(filename, 'w') as f:
        f.write(html)
    return "https://www.qicycling.cn/html/_" + str(article_id) + '.html'

def post_to_search(article_id, title, description, h5, author):
    url = "http://47.97.124.47:8085/qicycling_root/api/solr/saveResource"
    headers = {'Content-type': 'application/json'}
    dict = {"resourceId":str(article_id),"title":title,"description":description,"h5url":h5,"publisher":author,"type":"0"}
    r = requests.post(url, data=json.dumps(dict), headers=headers)
    print r.text
    return r

def recordArticle(db_app, articles):
    cursor_app = db_app.get_cursor()
    cursor_wp = db_wp.get_cursor()
    try:
        for article in articles:
            article_id = int(article['article_id'])
            img_url = article['src']
            title = article['alt']
            description = article['text']
            href = article['href']
            #print("--------- todo article:%d"%article_id)

            cursor_app.execute("SELECT status FROM resource where id=%d"%article_id)
            result = cursor_app.fetchone()
            if result is None:
                html, img_list, author, v_list = get_href(href)

                # 时间从 db_wp 读取 wp_posts.id =
                if len(img_list) <= 0:
                    img_ = Image.open(requests.get(img_url, stream=True).raw)
                    width, height = img_.size
                    pinfo = {'url': img_url, 'width': int(width), 'height': int(height)}
                    img_list.append(pinfo)

                cursor_wp.execute("SELECT UNIX_TIMESTAMP(post_date) FROM wp_posts where id=%d" % article_id)
                result = cursor_wp.fetchone()
                ts = result[0]
                # print article_id, img_list, author, title, description, ts
                h5 = save_h5(html, article_id)

                sql = "INSERT INTO resource (id, title, description, status, h5url, is_vip, publisher, type,TIMESTAMP)" \
                        " VALUES (%d, '%s', '%s', 1, '%s', 0, '%s', 0, %d)" % (article_id, title, description, h5, author, ts*1000)
                cursor_app.execute(sql)

                if(len(v_list)>0):
                    v_url = quote(v_list[0])
                    #v_url = quote(v_list[0])
                    sql = "UPDATE resource set video_url='%s' where id=%d"%(v_url,article_id)
                    #print sql
                    cursor_app.execute(sql)

                for i in xrange(len(img_list)):
                    img = img_list[i]
                    #surl = quote(img['url'])
                    surl = img['url']
                    sql = "INSERT INTO resource_image (resource_id, height, `length`, url) values (%d,%d,%d,'%s')"%(article_id,int(img['width']),int(img['height']),surl)
                    cursor_app.execute(sql)

                # post to
                post_to_search(article_id, title, description, h5, author)
            else:
                #print("article_id:%d already exists."%article_id)
                continue

            # 修改赛事类型
            sql2 = "select ter.name, r.`object_id`, tax.taxonomy  from wp_term_taxonomy tax inner join wp_terms ter on ter.`term_id` = tax.term_id" \
                            " inner join `wp_term_relationships` r on r.`term_taxonomy_id` = tax.`term_taxonomy_id`" \
                            " where taxonomy = 'category' and r.`object_id` = %d"%article_id
            cursor_wp.execute(sql2)
            r2 = cursor_wp.fetchone()
            if r2 is None:
                log.error("------ article:%d not found category")
            else:
                name = r2[0]
                sql = "SELECT id FROM `module` where name='%s'"%name
                #print sql
                cursor_app.execute(sql)
                r = cursor_app.fetchone()
                if r is not None:
                    module_id = int(r[0])
                else:
                    #
                    t = time.time()
                    ts = int(round(t * 1000))
                    cursor_app.execute("INSERT INTO `module` (status, description, display_order, name, resource_type, parent_id, timestamp)" \
                                   " values (1, '%s', 20, '%s', 1, 1, %d)" % (name, name, ts))
                    module_id = int(cursor_app.lastrowid)
                cursor_app.execute("INSERT INTO module_resource (status, module_id, resource_id, `timestamp`) " \
                               "VALUES (1, %d, %d, %d)"%(module_id, article_id, ts))

        db_app.commit()
        db_wp.commit()
    except Exception, e:
        log.error(e.message)
        log.error(traceback.format_exc())


def redoHtml(articles):
    for article in articles:
        article_id = int(article['article_id'])
        print article_id
        href = "http://www.qicycling.cn/" + str(article_id) + ".html"
        html, img_list, author, v_list = get_href(href)
        h5 = save_h5(html, article_id)

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
    #post_to_search(3448, '环阿尔卑斯S5：帕登为巴林美利达车队带来大丰收', '环阿尔卑斯S5：帕登为巴林美利达车队带来大丰收', 'http://www.qicycling.cn/html/_3448.html', 'guyyu')
    #'''
    banners = getBanner(config.web_url)
    #print banners
    recordBanner(db_app, banners)

    page = 0
    while(True):
        page += 1
        articles = getArticle(page)
        if len(articles) <= 0:
            break
        recordArticle(db_app, articles)
        #redoHtml(articles)
        print("---------------- getArticle page:%d Done."%page)
    #'''
    #print  getArticle(2)
    # 3696 text
    # 3366 video
    #html, img_list, author, video_list = get_href('http://www.qicycling.cn/3696.html')
    #print html
    # print author

