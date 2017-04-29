import unittest
import Constants
from Classes import LocalService

class TestServiceDiscovery(unittest.TestCase):

    def test_local(self):
        s1 = LocalService()
        s2 = LocalService(port = 337, name = 'local_337')

        self.assertEqual(s1.port, Constants.DEFAULT_SERVICE_PORT)
        self.assertEqual(s2.port, 337)

if __name__ == '__main__':
    unittest.main()
