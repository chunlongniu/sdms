#-*-coding:utf-8-*-
import os
import sys
import json
import logging
import MySQLdb.cursors as cursors
from core import sdmsdb 
from core.sdmslog import SdmsLogger

reload(sys)
sys.setdefaultencoding("utf-8")

logger = SdmsLogger(__name__)
logger.setLevel(logging.DEBUG)


class Station(object):

    def __init__(self):
        pass

    def __str__(self):
        serial_obj = {}
        for key, value in self.__dict__.items():
            serial_obj[key] = str(value)
        return json.dumps(serial_obj, ensure_ascii=False)


class StationDao(object):

    def __init__(self, sql="MYSQL"):
        self._sql = sql

    def fetch_station(self, machine_id, loader_type="Loader"):
        sql_query = "SELECT * FROM stations WHERE %s = %d";
        logger.info(loader_type)
        if loader_type == "Loader":
            sql_query = sql_query % ("LoaderID", machine_id)
        if loader_type == "Unloader":
            sql_query = sql_query % ("UnloaderID", machine_id)

        machine = None
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            machine = cursor.fetchone()
        return self._wrap_object(machine)            
        
    def fetch_all_station(self, argk = None, index=0, limit=4):
        results = []
        criterial = self.compose_criterial(argk) 
        logger.info(criterial)
        sql_query = "SELECT * FROM stations limit %d, %d" % (index, limit)
        if criterial:
                sql_query = "SELECT * FROM stations WHERE 1 = 1 AND %s limit %d, %d" % (criterial, index, limit)

        return self._execute_fetch_query(sql_query)

    def compose_criterial(self, argk):
        sql_query = [] 
        if argk:
            for key, value in argk.items():
                sql_query.append(" %s like '%%%s%%' " % (key, value))

        return "OR".join(sql_query)
    
    def _wrap_objects(self, results):
        for result in results:
            yield self._wrap_object(result)            

    def _wrap_object(self, result): 
        station = Station()
        for key, value in result.items():
            setattr(station, key, value)

        return station

    def fetcn_station_by_ids(self, ids, index = 0, limit=4):
        results = []
        logger.info("Fetch station information by " +  str(ids))
        sql_query = "SELECT * FROM stations  limit %d , %d"

        if ids:
            sql_query = "SELECT * FROM stations where LineId in %s limit %d , %d" % (ids, index, limit)
        logger.debug(sql_query)

        return self._execute_fetch_query(sql_query)

    def _execute_fetch_query(self, sql_query):
        with sdmsdb.connection() as con: 
            cursor = con.cursor(cursors.DictCursor)
            cursor.execute(sql_query)
            results = cursor.fetchall()
        return self._wrap_objects(results)

    def fetch_station_by_type(self, station_type):
        sql_query = "SELECT DISTINCT(%s), LoaderID, UnloaderID, LineID, LineType, LoaderStatus, UnloaderStatus from stations" % station_type
        return self._execute_fetch_query(sql_query)

