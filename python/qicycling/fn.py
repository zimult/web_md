import logging
from logging.handlers import TimedRotatingFileHandler
import db
import config


formatter = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
fileTimeHandler = TimedRotatingFileHandler('./log/' + 'sync', "d", 1, 30)
fileTimeHandler.suffix = "%Y%m%d.log"
logging.basicConfig(level = logging.INFO)
fileTimeHandler.setFormatter(formatter)
log.addHandler(fileTimeHandler)

db_wp = db.DB(config.host, config.user, config.password, config.database_wp)
db_app = db.DB(config.host, config.user, config.password, config.database_app)