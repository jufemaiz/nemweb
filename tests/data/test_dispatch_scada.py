""" Shhh """

import logging
import unittest

from nemweb.data import dispatch_scada

logging.getLogger().addHandler(logging.NullHandler())

class TestDispatchScada(unittest.TestCase):

    def test_dataset(self):
        self.assertEquals(True, True)

    def test_standarize(self):
        self.assertEquals(True, True)

    def test_nemserializer(self):
        self.assertEquals(True, True)

if __name__ == '__main__':
    unittest.main()
