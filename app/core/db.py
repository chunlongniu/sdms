import os
import sys
import hashlib
from contextlib import contextmanager as ctx
import sqlite3

_CUR_PATH = os.getcwd() 
_DB_PATH = os.path.join(_CUR_PATH, "data", "sdms.db")
#_DB_PATH = os.path.join(_CUR_PATH, "data", "..", "sdms.db")


def encrypt_passwd(passwd):
    entryption_passwd = hashlib.sha1(passwd).hexdigest()
    return entryption_passwd

def generate_database():
    connection = sqlite3.connect(_DB_PATH)
    cur = connection.cursor()
    cur.executescript(_DB_SCHEMA)

def show_tables():
    connection = sqlite3.connect(_DB_PATH)
    cur = connection.cursor()
    cur.execute("SELECT name FROM sqlite_master where type='table'")
    result = cur.fetchall()
    print result

class Connection(object):

    def __init__(self, **argk):
        self._free = True 
        self.connection = sqlite3.connect(_DB_PATH, check_same_thread=False)

    def fetch_all(self, query):
        result = []
        try:
            cur = self.connection.cursor()
            cur.execute(query)
            result = cur.fetchall()
        except sqlite3.Error as e:
            print "Query [ %s ] Error occured %s" % (query, str(e))
        finally:
            return result

    def fetch_one(self, query, parameters):
        result = None
        cur = self.connection.cursor()
        try:
            cur.execute(query, parameters)
            print query
            print parameters
            result = cur.fetchone()
        except sqlite3.Error as e:
            print "Query [ %s ] Error occured %s" % (query, str(e))
        finally:
            cur.close()
            return result

    def delete(self, query):
        try:
            cur = self.connection.cursor()
            cur.execute(query) 
        except sqlite3.Error as e:
            print "Query [ %s ] Error occured %s" % (query, str(e))
        finally:
            return result

    def update(self, query):
        result = None
        try:
            cur = self.connection.cursor()
            cur.execute(query)
        except sqlite3.Error as e:
            print "Query [ %s ] Error occured %s" % (query, str(e))
        finally:
            return result

    @property
    def is_free(self):
        return self._free
    
    @is_free.setter
    def is_free(self, free=True):
        self._free = free 

    def __del__(self):
        self._free = True

class ConnectionFactory(object):

    def __init__(self, **argk):
        super(ConnectionFactory, self).__init__(**argk) 
        self._instance = None
        self._pool = []
        self._max_size = 20 
        self._initilize_pool()

    @property
    def fectory(self):
        return self._instance

    def _initilize_pool(self):
        while self._max_size: 
            connection = Connection()
            self._pool.append(connection)
            self._max_size -= 1

    def get_connection(self):
        for con in self._pool:
            if con.is_free:
                con.is_free = False
                return con
        else:
            return None

    def get_pool(self):
        return self._pool

    def __call__(self,*argc, **argk):
        if cls._instance is None: 
            cls._instance = super(ConnectionFactory, self).__call__(*argc, **argk)
        return self._instance

_fectory = ConnectionFactory()

@ctx
def connection():
    con = _fectory.get_connection()
    yield con
    con.is_free = True

_DB_SCHEMA ="DROP TABLE IF EXISTS user; \
             CREATE TABLE IF NOT EXISTS user \
             (id INTEGER PRIMARY KEY NOT NULL, \
              name VARCHAR(32) NOT NULL,\
              password VARCHAR(32) NOT NULL,\
              role CHAR NOT NULL,\
              avaiable BOOL NOT NULL\
             );\
             DROP TABLE IF EXISTS product; \
             CREATE TABLE IF NOT EXISTS product \
             ( prod_no VARCHAR(16) PRIMARY KEY NOT NULL,\
               prod_name VARCHAR(32) NOT NULL, \
               description VARCHAR(50) \
             ); \
             DROP TABLE IF EXISTS passage; \
             CREATE TABLE IF NOT EXISTS passage \
             ( id INTEGER PRIMARY KEY NOT NULL,\
               prod_no VARCHAR(16) NOT NULL, \
               passage INTEGER NOT NULL, \
               datetime timestamp NOT NULL, \
               FOREIGN KEY (prod_no) REFERENCES product(prod_no) ON DELETE CASCADE\
             ); \
             INSERT INTO user VALUES(NULL, 'admin', '%s', 'admin', 'true')\
             " % encrypt_passwd("tester")

if __name__ == "__main__":
    generate_database()
    show_tables()

