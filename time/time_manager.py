import datetime as _DT
import threading as _TH

REAL = 1
SIMULATED = 2
_mode = REAL
datetime = _DT.datetime
timedelta = _DT.timedelta
_cur = datetime.now()
_timers = []
_ratio = 0.0
_start = datetime.now()

def _now_sim():
    return _cur

def _now_ratio():
    global _start
    global _ratio
    return _cur + _DT.timedelta(seconds = (datetime.now() - _start).total_seconds() * _ratio)

now = datetime.now

class _ratio_timer(_TH.Timer):

    def __init__(self, interval, callback, args=None, kwargs=None):
        global _ratio
        global _timers
        _TH.Timer.__init__(self, interval / _ratio, callback, args, kwargs)
        _timers.append(self)


class _real_timer(_TH.Timer):

    def __init__(self, interval, callback, args=None, kwargs=None):
        global _timers
        _TH.Timer.__init__(self, interval, callback, args, kwargs)
        _timers.append(self)


Timer = _real_timer

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
    t = _TH.Timer(secs, _dummy)
    t.start()
    t.join()

def _wait_ratio(secs):
    global _ratio
    _wait_real(secs / _ratio)

def _wait_sim(secs):
    global _cur
    global _timers
    if secs <= 0:
        return
    _cur = _cur + _DT.timedelta(seconds=secs)
    for timer in sorted(filter(lambda t : t._state == _simulated_timer.RUNNING and t._elapsed_date <= _cur, _timers), key=lambda t : t._elapsed_date):
        timer._fire()
        _timers.remove(timer)


def _wait_until_real(stop_time):
    _wait_real((stop_time - datetime.now()).total_seconds())

def _wait_until_ratio(stop_time):
    global _ratio
    _wait_real((stop_time - now()).total_seconds() / _ratio)

def _wait_until_sim(stop_time):
    global _cur
    _wait_sim((stop_time - _cur).total_seconds())

wait = _wait_real
wait_until = _wait_until_real

def set_sim(start = None, ratio = None):
    global _mode
    global _cur
    global _timers
    global Timer
    global now
    global wait
    global wait_until
    global _ratio
    global _start
    _ratio = ratio
    _mode = SIMULATED
    _cur = datetime.now() if start == None else start
    for timer in _timers:
        timer.cancel()
    _timers = []
    _start = datetime.now()
    Timer = _simulated_timer if ratio == None else _ratio_timer
    now = _now_sim if ratio == None else _now_ratio
    wait = _wait_sim if ratio == None else _wait_ratio
    wait_until = _wait_until_sim if ratio == None else _wait_until_ratio


def set_real():
    global _mode
    global _timers
    global Timer
    global now
    global wait
    global wait_until
    _mode = REAL
    for timer in _timers:
        timer.cancel()
    _timers = []
    Timer = _real_timer
    now = datetime.now
    wait = _wait_real
    wait_until = _wait_until_real
