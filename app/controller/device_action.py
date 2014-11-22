import sys
import logging
import json
from core import app
from jinja2 import Template
from controller import view
from jinja2 import Environment, PackageLoader
from bottle import request, redirect
from models.sdms_machine import MachineDao
from models.sdms_station import StationDao
from core.sdmslog import SdmsLogger


logger = SdmsLogger(__name__)
logger.setLevel(logging.DEBUG)

class DeviceException(Exception):
    pass

class DeviceInfo(object):

    def __init__(self):
        pass

    def __str__(self):
        serial_obj = {}
        for key, value in self.__dict__.items():
            serial_obj[str(key)] = str(value)
        return json.dumps(serial_obj, ensure_ascii=False)

class DeviceAction(object):

    def __init__(self):
        self._station_dao = StationDao()
        self._machine_dao = MachineDao()

    def fetch_machine_by_id(self, machine_id):
        machine_dao = MachineDao()
        return machine_dao.fetch_machine(machine_id)
        
    def fetch_device_info(self):
        stations = self._get_stations()
        return self._fetch_machines(stations)

    def _fetch_machines(self, stations):
        results = {"WorkShop":[], "LineType":[]} 
        for m_type, station_list in stations.items():
            for station in station_list: 
                results[m_type].append(self._filter_info(station, m_type)) 
        return results 

    def _filter_info(self, station, m_type):
        device_info = DeviceInfo() 
        device_info.m_type = m_type 
        if hasattr(station, "LineType"):
            device_info.cat_name = station.LineType
        if hasattr(station, "WorkShop"):
            device_info.cat_name = station.WorkShop
        machine = None
        if not machine:
            machine = self._machine_dao.fetch_machine_criterial('Loader', station.LoaderID)
        else:
            machine = self._machine_dao.fetch_machine_criterial('Unloader', station.LoaderID)
         
        if machine:
            device_info.machine = machine.MachineName
            device_info.machine_id = machine.MachineID
            device_info.line_id = station.LineID
            device_info.line_type = station.LineType
            device_info.loader_status = station.LoaderStatus
            device_info.unloader_status = station.UnloaderStatus
        return device_info
    
        
    def _get_stations(self):
        stations = {} 
        for device_type in ("LineType", "WorkShop"):
            device = self._station_dao.fetch_station_by_type(device_type)
            stations[device_type] = device
        return stations 

import json

@app.route("/sdms/device/loader", method='GET')
@view("device_info.html")
def _fetch_device():
    device_act = DeviceAction()
    results = device_act.fetch_device_info()
#    _print(results)
    return results

def _print(results):
    fmt = "{:<8} {}"
    for key, values in results.items():
        for value in values:
             logger.info(fmt.format(key, str(value)))

