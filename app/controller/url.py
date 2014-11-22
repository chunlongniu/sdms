# -*- coding: utf-8 -*-,

import sys
from core import app
from jinja2 import Template
from controller import view
from jinja2 import Environment, PackageLoader

#import control as ctl

env = Environment

class DeviceInfo(object):

    def __init__(self):
        pass

device_info_list = [] 

for index in range(8):
    device = DeviceInfo()
    device.name = "name" + str(index)
    device.device_type = "device_type" + str(index)
    device.status = "status" + str(index)
    device.device_name = "device_name" + str(index)
    device.time = "time" + str(index)
    device_info_list.append(device)

from time import sleep
@app.route("/main", name="main")
@view("main.html")
def main():
	return {"message":"HelloWord"}

@app.route("/deviceinfo")
@view("device.html")
def device_info():
    return {"device_list":device_info_list}

@app.route("/intension")
@view("intension.html")
def intension_info():
    return {}

@app.route("/")
@view("login.html")
def main_page():
    return {}

@app.post("/login")
@app.get("/login")
@view("login.html")
def login():
	return {}
#   return ctl.authorize_user()

@app.get("/device_status")
@view("device_status.html")
def device_status():
    return {}

@app.get("/device_info")
@view("device_info.html")
def device_status():
    return {}

@app.get("/alarm_active")
@view("alarm_active.html")
def alarm_active():
    return {}
