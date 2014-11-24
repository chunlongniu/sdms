# -*- coding: utf-8 -*-
import os
import sys
import signal
import logging
from bottle import run
from bottle import static_file
from bottle import CherryPyServer
from controller import *
from core import app
from core.sdmslog import SdmsLogger 


#Define primary constant variables 

_CUR_PATH = os.getcwd()
#sys.path.append(_CUR_PATH)
_STATIC_PATH = os.path.join(_CUR_PATH, "static")
_DATA_PATH = os.path.join(_CUR_PATH, "data")
_OPTIONS = {
    "numthreads":10,
    "max":1000,
    "shutdown_timeout":5
}

logger = SdmsLogger(__name__)
logger.setLevel(logging.DEBUG)

#Add file and images filter 

@app.route("/static/<filename:re:.*>")
def server_static(filename):
    return static_file(filename, root = _STATIC_PATH)

@app.route("/data/<filename:re:.*>")
def data_path(filename):
    return static_file(filename, root = _DATA_PATH)


#Main function of project

def start():
    logger.info("Server started ...")
    try:
        server = CherryPyServer(host="0.0.0.0", port="8888")
        server.run(app)
    except KeyboardInterrupt:
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)
        logger.info("Server down ...")
