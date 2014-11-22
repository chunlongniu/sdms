#-*-coding:utf-8-*-
import os
import sys
import json
import logging
import MySQLdb.cursors as cursors
from core.sdmslog import SdmsLogger
from core import sdmsdb 

reload(sys)
sys.setdefaultencoding("utf-8")

logger = SdmsLogger(__name__)
logger.setLevel(logging.DEBUG)


class Machine(object):

    def __init__(self):
        pass

    def __str__(self):
        serial_obj = {}
        for key, value in self.__dict__.items():
            serial_obj[str(key)] = str(value)
        return json.dumps(serial_obj, ensure_ascii=False)

class MachineDao(object):

    def __init__(self, sql="MYSQL"):
        self._sql = sql

    def fetch_machine(self, machine_id):
        sql_query = "SELECT * FROM machines where MachineID = " +  str(machine_id)
        machine = {}
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            machine = cursor.fetchone()
        return self._wrap_object(machine)

    def fetch_all_machine(self, index=0, limit=5, **argk):
        sql_query = "SELECT * FROM machines limit %d, %d"% (index, limit)
        return self._execute_sqlquery(sql_query)

    def fetch_machine_criterial(self, m_type, machine_id):
        sql_query = "SELECT  * FROM machines WHERE MachineID = '%s' AND MachineClass = '%s'" % (machine_id, m_type) 
        result = {}
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            result = cursor.fetchone()
             
        if result:
            result = self._wrap_object(result)
        return result
    
    def _wrap_objects(self, results):
        for result in results:
            yield self._wrap_object(result)            

    def _wrap_object(self, result): 
        machine = Machine()
        for key, value in result.items():
            setattr(machine, key, value)
        return machine 

    def _execute_sqlquery(self, sql_query):
        results = []
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            results = cursor.fetchall()
        return self._wrap_objects(results)
