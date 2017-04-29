import time_manager as tm
import unittest

class TestTimeModes(unittest.TestCase):

    def setUp(self):
        # tolerance interval in seconds
        self.delta = 0.05

        # wait duration
        self.wait = 5.0

        # timer intervals
        self.int1 = 1.0
        self.int2 = 2.0

    def __inner_func(self):

        # store start time
        start = tm.now()
        end = start + tm.timedelta(seconds = self.wait)

        # flags
        t1elapsed = False
        t2elapsed = False

        # timer callbacks
        def t1callback():
            nonlocal t1elapsed
            t1elapsed = True

        def t2callback():
            nonlocal t2elapsed
            t2elapsed = True

        t1 = tm.Timer(self.int1, t1callback)
        t2 = tm.Timer(self.int2, t2callback)

        t1.start()
        t2.start()

        # wait half the interval for t1 - no timer elapsed
        tm.wait(self.int1 / 2.0)
        self.assertFalse(t1elapsed, "t1 should not have elapsed")
        self.assertFalse(t2elapsed, "t2 should not have elapsed")

        # wait half the interval for t1 + half for t2 - t1 elapsed, t2 not elapsed
        tm.wait(self.int2 / 2.0)
        self.assertTrue(t1elapsed, "t1 should have elapsed")
        self.assertFalse(t2elapsed, "t2 should not have elapsed")

        # wait until the end - noth timers elapsed
        tm.wait_until(end)
        self.assertTrue(t1elapsed, "t1 should have elapsed")
        self.assertTrue(t2elapsed, "t2 should have elapsed")

        # check end date
        self.assertTrue(abs((tm.now() - end).total_seconds()) < self.delta, "end time is wrong")

    def test_real(self):

        # set system clock management
        tm.set_real()

        # call inner function
        self.__inner_func()

    def test_sim(self):

        # set system clock management
        tm.set_sim()

        # call inner function
        self.__inner_func()

    def test_ratio(self):

        # set system clock management
        tm.set_sim(ratio = 10.0)

        # call inner function
        self.__inner_func()

if __name__ == '__main__':
    unittest.main()

