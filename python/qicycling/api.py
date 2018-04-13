# -*- coding: utf-8 -*-

#import logging
#from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
import db
import sync


shorty_api = Flask(__name__)

db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
db_app = db.DB(config.host, config.user, config.password, config.database_app)

@shorty_api.route('/get_cartoon_material', methods=['GET', 'POST'])
def get_cartoon_material():
    return "haah"

@shorty_api.route('vip_article', methods=['GET', 'POST'])
def vip_article():
    return "haah"

if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8410 )