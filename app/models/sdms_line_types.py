#-*-coding:utf-8-*-
import os
import sys
import logging
import MySQLdb.cursors as cursors
from sdmslog import SdmsLogger
import sdmsdb 

reload(sys)
sys.setdefaultencoding("utf-8")

logger = SdmsLogger(__name__)
logger.setLevel(logging.DEBUG)


class LineType(object):

    def __init__(self):
        pass

    def __str__(self):
        return repr(self.__dict__)

    def get_attr_value(self):
        return self.__dict__

class LineTypeDao(object):

    def __init__(self, sql="MYSQL"):
        self._sql = sql

    def fetch_linetype(self):
        pass

    def save(self, linetype):
        sql_query = "INSERT INTO machine_types (%s) VALUES (%s)" % (self.__extract_args(machine))
        with sdmsdb.connection() as con: 
            cursor = con.cursor()
            cursor.execute(sql_query)
            con.commit()
        
        logger.info(sql_query)
         
    def __extract_args(self, linetype):
        columns, values = [], []
        for attr, value in linetype.get_attr_value().items():
            columns.append(attr)
            values.append(value)

        return self.__format_column(columns), self.__format_values(values)
        
        
    def __format_values(self, values):
        fmt = lambda x:"'%s'"%(x)
        fmt_values = [fmt(value) for value in values]
        return ", ".join(fmt_values)

    def __format_column(self, columns):
       return ", ".join(columns)  

    def fetch_all_linetype(self, index=0, limit=5, **argk):
        sql_query = "SELECT * FROM line_types limit %d, %d"% (index, limit)
        results = []
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            results = cursor.fetchall()
        return self._wrap_objects(results)
    
    def _wrap_objects(self, results):
        for result in results:
            yield self._wrap_object(result)            

    def _wrap_object(self, result): 
        line_type = LineType()
        for key, value in result.items():
            setattr(line_type, key, value)

        return line_type 

if __name__ == "__main__":
    line_type_dao = LineTypeDao()        
    results = line_type_dao.fetch_all_linetype()
    for result in results:
        print(str(result.LineType))
