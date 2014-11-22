import sys
import logging
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

class MachineException(Exception):
    pass

class MachineAction(object):

    def __init__(self):
        pass

    def find_all(fetch):
        machine_dao = MachineDao()
        #types = unicode(request.query.get("type_s"), "utf-8")
        return machine_dao.fetch_all_station(args)

    def fetch_machine_by_id(self, machine_id):
        machine_dao = MachineDao()
        return machine_dao.fetch_machine(machine_id)
        

    def fetch_name_by_type(self):
        return None


@app.route("/sdms/machine/<operation>/<machine_id>", method='GET')
def _fetch_machine(operation, machine_id):
    logging.info("Fetch machine by : " + machine_id)
    machine = {};
    if operation == "fetch":
        try:
            machine_act = MachineAction()
            _id = int(machine_id)
            machine = machine_act.fetch_machine_by_id(_id)
            station = _get_station(machine.MachineClass, _id)
        except ValueError as e:
            pass
    return str(machine)

def _get_station(machine_class, machine_id):
    station_dao = StationDao()
    return station_dao.fetch_station(machine_id, machine_class)
