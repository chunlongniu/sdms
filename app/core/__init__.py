from bottle import Bottle
from beaker.middleware import SessionMiddleware
import bottle

_session_opts = {
    "session.type": "file",
    "session.cookie_expires":300,
    "session.data_dir": "./data",
    "session.auto":True
}

app = bottle.default_app()
