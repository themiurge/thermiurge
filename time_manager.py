import datetime as _DT
import threading as _TH

REAL = 1
SIMULATED = 2
_mode = REAL
datetime = _DT.datetime
Timer = _TH.Timer
_cur = datetime.now()
_timers = []

def _now_sim():
    return _cur

now = datetime.now

class _simulated_timer:
    INITIALIZED = 1
    RUNNING = 2
    STOPPED = 3

    def __init__(self, interval, callback, args=None, kwargs=None):
        self.interval = interval
        self.callback = callback
        self.args = [] if args == None else args
        self.kwargs = {} if kwargs == None else kwargs
        self._state = _simulated_timer.INITIALIZED
        self._elapsed_date = None
        _timers.append(self)

    def start(self):
        if self.interval <= 0:
            self._state = _simulated_timer.STOPPED
            return
        self._state = _simulated_timer.RUNNING
        self._elapsed_date = now() + _DT.timedelta(seconds = self.interval)

    def cancel(self):
        self._state = _simulated_timer.STOPPED

    def _fire(self):
        self.callback(*(self.args), **(self.kwargs))
        self._state = _simulated_timer.STOPPED

def _wait_real(secs):
    if secs <= 0:
        return
    def _dummy():
        pass
    t = Timer(secs, _dummy)
    t.start()
    t.join()

def _wait_sim(secs):
    global _cur
    global _timers
    if secs <= 0:
        return
    _cur = _cur + _DT.timedelta(seconds=secs)
    for timer in sorted(filter(lambda t : t._state == _simulated_timer.RUNNING and t._elapsed_date <= _cur, _timers), key=lambda t : t._elapsed_date):
        timer._fire()
        _timers.remove(timer)

wait = _wait_real

def set_sim(start):
    global _mode
    global _cur
    global _timers
    global Timer
    global now
    global wait
    _mode = SIMULATED
    _cur = start
    _timers = []
    Timer = _simulated_timer
    now = _now_sim
    wait = _wait_sim
