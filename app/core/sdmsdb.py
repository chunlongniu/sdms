import sys
import copy
import logging
from sdmslog import SdmsLogger 
from contextlib import contextmanager

logger = SdmsLogger()
logger.setLevel(logging.DEBUG)

_DEFAULT_SQL_NAME= "MYSQL"

class Connection(object):

    def __init__(self):
        self._occupied = False

    def create(self, **argk):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    @property
    def occupied(self):
        return self._occupied

    @occupied.setter
    def occupied(self, occupied):
        self._occupied = occupied

   
try:
    import MySQLdb
except ImportError as e:
    logger.error(str(e))     
    

mysql_config = {
    "host":"127.0.0.1",
    "port":3306,
    "dbname":"nodefw",
    "user":"root",
    "passwd":"1234"

}

class MySQLConnection(Connection):

    def __init__(self):
        self._connection = None
        self._occupied = False
        self._config = copy.deepcopy(mysql_config)

    def create(self, **argk):
        config = self._filter_config(**argk)                       
        self._connection = MySQLdb.connect(host=config['host'],
                                          user=config['user'],
                                          passwd=config['passwd'],
                                          db=config['dbname'],
                                          port=config['port'],
                                          charset='utf8'
                                          )
        return self._connection
        

    def _filter_config(self, **argk):
        for key, value in argk:
            if self._config.has_key(key):
                self._config[key] = value
        return self._config 

    def close(self):
        if self._connection:
            self._connection.close()
        logger.debug("connection closed")

SQL_LIST = {"MYSQL": MySQLConnection()}

@contextmanager
def connection(sql = _DEFAULT_SQL_NAME):
    logger.debug("%s is used in program", sql)
    mysql_con = None
    if SQL_LIST.has_key(sql): 
        mysql_con = SQL_LIST[sql] 
        yield mysql_con.create()
    if mysql_con:
        mysql_con.close()

def test():
    
    logger.debug("Test")
