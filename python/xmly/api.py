# -*- coding: utf-8 -*-

#import logging
#from logging.handlers import TimedRotatingFileHandler

from flask import Flask
import config
#import db
import requests
from flask import request, redirect

shorty_api = Flask(__name__)

# db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
# db_app = db.DB(config.host, config.user, config.password, config.database_app)

@shorty_api.route('/redirect_uri', methods=['GET', 'POST'])
def redirect_uri():
    id = int(request.values.get('id'))
    print id
    return "haah"

if __name__ == '__main__':
    shorty_api.run(host='0.0.0.0', port=8410 )
