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


class Alarm(object):

    def __init__(self):
        pass

    def __str__(self):
        serial_obj = {}
        for key, value in self.__dict__.items():
            serial_obj[str(key)] = str(value)
        return json.dumps(serial_obj, ensure_ascii=False)

class AlarmDao(object):

    def __init__(self, sql="MYSQL"):
        self._sql = sql

    def fetch_alarm(self):
        pass

    def get_alarm_num(self):
        count  = 0
        sql_query = "SELECT count(*) FROM alarms"
        with sdmsdb.connection() as con: 
            cursor = con.cursor()
            cursor.execute(sql_query)
            count = cursor.fetchone()
        
        return count

    def fetch_all_alarms(self, index=0, limit=7, **argk):
        sql_query = "SELECT * FROM alarms limit %d, %d"% (int(index), int(limit))
        results = []
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            results = cursor.fetchall()
        return self._wrap_objects(results)

    def fetch_alarm_by_id(self, alarm_id):
        sql_query = "SELECT * FROM alarms WHERE AlarmID = %d" % int(alarm_id)
        result = None
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            result = cursor.fetchone()
        return self._wrap_object(result)

    def fetch_alarms_by_machineid(self, machine_id, index=0, limit=7):
        sql_query = "SELECT * FROM alarms WHERE MachineID=%d limit %d, %d" % (machine_id, index, limit)
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            results = cursor.fetchall()
        return self._wrap_objects(results)


    
    def _wrap_objects(self, results):
        for result in results:
            yield self._wrap_object(result)            

    def _wrap_object(self, result): 
        alarm = Alarm()
        for key, value in result.items():
            setattr(alarm, key, value)

        return alarm 
