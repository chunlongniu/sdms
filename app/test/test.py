import threading
from time import sleep
from contextlib import contextmanager as ctx
class A(object):

    def __init__(self):
        self.is_free = True 

    def print_out(self):
        print "HelloWord"

pool = []
for a in range(3):
    pool.append(A())

def get_instance():
    global pool
    for con in pool:
        con.is_free =False
        return con

from time import sleep

@ctx
def use_con():
    con = get_instance()
    yield con
    con.is_free = True 

with use_con() as con:
    con.print_out()

for con in pool:
    print con.is_free

