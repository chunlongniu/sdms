from contextlib import contextmanager as ctx
from __future__ import with_statement 

@ctx
def show():
    print "HelloWord"
    yield 
    print "Finished"

with show:
    print s

