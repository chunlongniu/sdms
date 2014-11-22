import sys
import logging
import json
from core import app
from jinja2 import Template
from controller import view
from jinja2 import Environment, PackageLoader
from bottle import request, redirect
from models.sdms_alarm import AlarmDao
from models.sdms_station import StationDao
from models.sdms_machine import MachineDao
from core.sdmslog import SdmsLogger


logger = SdmsLogger(__name__)
logger.setLevel(logging.DEBUG)
_PAGE_LIMIT = 7

class AlarmException(Exception):
    pass

class AlarmAction(object):

    def __init__(self):
        self.alarm_dao = AlarmDao()

    def find_all_alarms(self, index = 0):
        results = []
        results = self.alarm_dao.fetch_all_alarms(index = index)
        return results


    def find_device_information(self, alarm_id):
        return self.alarm_dao.fetch_alarm_by_id(alarm_id)


    def find_alarm_by_machineid(self, machine_id):
        results = self.alarm_dao.fetch_alarms_by_machineid(machine_id, index=0, limit=8)
        return results 
        
    def get_alarm_count(self):
        count =  self.alarm_dao.get_alarm_num()
        return max(count)

    def _compose_criterial(self):
        pass        


@app.route("/sdms/alarm_active/<operation>", method='GET')
@view("alarm_active.html")
def _alarm_info(operation):
    alarm_act = AlarmAction()
    index, cur_page, alarms = 0, 1, []
    logger.info("Fetch all alarm active information ...")

    if "cur_page" in request.query.keys():
        cur_page = request.query.cur_page
        index = (int(cur_page) - 1) * _PAGE_LIMIT 
    count = alarm_act.get_alarm_count()
    for alarm in alarm_act.find_all_alarms(index):
        alarms.append(alarm)

    total_page = int(count/_PAGE_LIMIT) + 1
    logger.info("Fetch all alarm active information successfully")

    return {"alarms":alarms, "cur_page":int(cur_page), "total_page":total_page}

@app.route("/sdms/alarm_active/<alarm_id:int>/<machine_id:int>", method='GET')
def _device_info(alarm_id, machine_id):
    logging.info("Fetch machine by : " +str(machine_id))
    
    alarm_act = AlarmAction()
    alarm = alarm_act.find_device_information(alarm_id)
    machine = _get_machine(machine_id)
    station = _get_station(machine.MachineClass, machine_id)
    device_info = {"station":str(station), "machine": str(machine), "alarm":str(alarm)}
    return json.dumps(device_info, ensure_ascii=False) 

@app.route("/sdms/ajax_alarm/<machine_id:int>", method='GET')
def _alarm_info_by_id(machine_id): 
    alarm_act = AlarmAction()
    results = []
    alarms = alarm_act.find_alarm_by_machineid(machine_id)
    for alarm in alarms:
        results.append(str(alarm))
    return json.dumps(results, ensure_ascii=False)

def _get_station(machine_class, machine_id):
    station_dao = StationDao()
    logger.info("Fetch station by: " + str(machine_id))
    return station_dao.fetch_station(machine_id, machine_class)

def _get_machine(machine_id):
    machine_dao = MachineDao()
    logger.info("Fetch machine by: " + str(machine_id))
    return machine_dao.fetch_machine(machine_id) 

