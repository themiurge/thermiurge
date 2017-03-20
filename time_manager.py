import datetime as _DT
import threading as _TH

REAL = 1
SIMULATED = 2
_mode = REAL
datetime = _DT.datetime
Timer = _TH.Timer
_CUR_DT = _DT

class _simulated_datetime:
    def

class _simulated_timer:
    INITIALIZED = 1
    RUNNING = 2
    STOPPED = 3

    def __init__(self, interval, callback, args=None, kwargs=None):
        self.interval = interval
        self.callback = callback
        self.args = [] if args == None else args
        self.kwargs = {} if kwargs = None else kwargs
        self._state = INITIALIZED

    def start():
        

def set_mode(m):
    if m == REAL:
        Timer = __TH__.Timer
    else if m == SIMULATED:
        
