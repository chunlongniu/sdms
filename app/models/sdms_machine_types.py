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


class MachineType(object):

    def __init__(self):
        pass

    def __str__(self):
        return repr(self.__dict__)

    def get_attr_value(self):
        return self.__dict__

class MachineTypeDao(object):

    def __init__(self, sql="MYSQL"):
        self._sql = sql

    def fetch_machinetype(self):
        pass

    def save(self, machine_type):
        sql_query = "INSERT INTO machine_types (%s) VALUES (%s)" % (self.__extract_args(machine_type))
        with sdmsdb.connection() as con: 
            cursor = con.cursor()
            cursor.execute(sql_query)
            con.commit()
        
        logger.info(sql_query)
         
    def __extract_args(self, machine_type):
        columns, values = [], []
        for attr, value in machine_type.get_attr_value().items():
            columns.append(attr)
            values.append(value)

        return self.__format_column(columns), self.__format_values(values)
        
        
    def __format_values(self, values):
        fmt = lambda x:"'%s'"%(x)
        fmt_values = [fmt(value) for value in values]
        return ", ".join(fmt_values)

    def __format_column(self, columns):
       return ", ".join(columns)  

    def fetch_all_machinetype(self, index=0, limit=5, **argk):
        sql_query = "SELECT * FROM machine_types limit %d, %d"% (index, limit)
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
        machine_type = MachineType()
        for key, value in result.items():
            setattr(machine_type, key, value)

        return machine_type 

if __name__ == "__main__":
    machine_type_dao = MachineTypeDao()        
    machine_type = MachineType()
    machine_type.MachineClass="Loader"
    machine_type.MachineName="斜立式收板机350版"
    machine_type.MachineType="FW-UD602"
    machine_type_dao.save(machine_type)
