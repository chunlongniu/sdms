#-*-coding:utf-8-*-
import sys
import json
import logging
from jinja2 import Template
from controller import view
from jinja2 import Environment, PackageLoader
from bottle import request, response, redirect

from core import app
from models.sdms_station import Station
from models.sdms_station import StationDao
from core.sdmslog import SdmsLogger

logger = SdmsLogger(__file__)
logger.setLevel(logging.DEBUG)

class StationError(Exception):
    pass

class StationAction(object):

    def __init__(self):
        pass

    def find_station_status(self):
        #args = unicode(request.forms.get("type"), "utf-8"), request.forms.get("criterial")
        arg_names = ["search_type", "criterial"]
        stations = []
        _value, _type = None, None
        station_dao = StationDao()
        try:
            args = self.__handler_args(arg_names)

            if "index" in request.query.keys(): 
                args["index"] = request.query["index"] 
            _type = str(args.keys().pop())
            _value = str(args.values().pop())
            print _value
            logger.info("THe criterial is: " + str(args) + " and type is: " + _type)
            if "All" not in args.keys():
                stations = station_dao.fetch_all_station(args)
            else:
                args={"Workshop":args['All'], "LineType":args['All']}
                logger.info("THe criterial is: " + str(args))
                stations = station_dao.fetch_all_station(args)
        except KeyError as e:
            logger.debug("No Criterial : " + str(e))
            stations = station_dao.fetch_all_station()

        return {"criterial":_value, "stations":stations, "type":_type}
    
    def __handler_args(self, arg_names):
        values = [tuple([unicode(request.query[name], "utf-8") for name in arg_names])]
        criterial = dict(values)
        logger.debug("The criterial is: " + str(criterial))
        return criterial 
        
    def fetch_station_by_ids(self):
        ids = request.query.ids
        logger.info("Fetch stations by ids " + str(ids))
        station_dao = StationDao()
        return  station_dao.fetcn_station_by_ids(ids)

@app.route("/sdms/station_info/<operation>", method='GET')
@view("station_status.html")
def _station_info(operation):
    return _station_status(operation)

@app.route("/sdms/ajax_fetch/station_info/fetch", method='GET')
def _station_by_ids():
    station_act = StationAction()
    results = []
    logger.info("Fetch stations via ajax")
    stations = station_act.fetch_station_by_ids()
    for station in stations:
        results.append(str(station))
    return json.dumps(results, ensure_ascii=False) 

def _station_status(operation):
    station_act = StationAction()
    results = []
    logger.info("Fetch stations ...")
    if operation == "search":
        stations = station_act.find_station_status()
        results = _convert_iterate_to_array(stations)
    logger.info("Fetch stations successfully") 

    return {"station_list":results, "criterial":stations['criterial'], "type":stations['type']}

def _convert_iterate_to_array(stations):
    results = []
    for station in stations['stations']:
        logger.debug(station.Workshop)
        results.append(station)
    return results
