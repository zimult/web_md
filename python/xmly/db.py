import MySQLdb

class DB:
    conn = None
    host = None
    user = None
    password = None
    db = None

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def get_con(self):
        self.conn = MySQLdb.connect(self.host, self.user, self.password, self.db, charset="utf8")

    def get_cursor(self):
        try:
            self.conn.ping()
            #print "ping ok"
        except:
            self.conn = MySQLdb.connect(self.host, self.user, self.password, self.db, charset="utf8")

        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()