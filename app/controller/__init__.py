# -*- coding: utf-8 -*
import functools
from bottle import jinja2_view

view = functools.partial(jinja2_view, template_lookup=["templates"])
__all__ = ["url",
           "station_action",
           "alarm_action",
           "machine_action",
           "device_action",
          ]
