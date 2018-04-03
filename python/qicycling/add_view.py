#! /usr/bin/python
# encoding:utf-8

import db
import config

db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
cursor = db_wp.get_cursor()

# wp_postmeta post_id=xx,  meta_key='views'
cursor.execute("SELECT `id`, TIMESTAMPDIFF(DAY, post_date, now()) from wp_posts where post_type='post' and post_status='publish'")
result = cursor.fetchall()
for row in result:
    id = int(row[0])
    days = int(row[1])

    cursor.execute("SELECT meta_value FROM wp_postmeta WHERE post_id=%d and meta_key='views'"%id)
    result2 = cursor.fetchone()
    views = int(result2[0])

    # 
    cursor.execute("SELECT meta_value FROM wp_posts_views_bk where post_id=%d"%id)
    r2 = cursor.fetchone()
    if r2 is None:
        if days > 3:
            n_data = views+1
        else:
            n_data = int(views * 1.1)

        sql = "INSERT INTO wp_posts_views_bk (post_id, meta_value) values (%d, '%s')" %(id,str(n_data))
        cursor.execute(sql)
    else:
        o_data = int(r2[0])
        if days > 3:
            n_data = views+1
        elif (views - o_data) > 10:
            n_data = int((views-o_data)*2)
        else:
            n_data = int(views*1.02 + 1)

        cursor.execute("UPDATE wp_posts_views_bk set meta_value='%s' WHERE post_id=%d"%(str(n_data),id))

    cursor.execute("UPDATE wp_postmeta set meta_value='%s' WHERE post_id=%d and meta_key='views'"%(str(n_data),id))


db_wp.commit()
#db_wp.close()

