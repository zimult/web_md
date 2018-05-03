# -*- coding: utf-8 -*-

#import logging
#from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
import db
from flask import request
import sync

shorty_api = Flask(__name__)

db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
db_app = db.DB(config.host, config.user, config.password, config.database_app)

@shorty_api.route('/sync_article', methods=['GET', 'POST'])
def sync_article():
    article_id = int(request.values.get('article_id'))

    return str(article_id)

if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8410 )
