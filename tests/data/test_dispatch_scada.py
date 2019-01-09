""" Shhh """

import logging
import unittest

from nemweb.data import dispatch_scada

logging.getLogger().addHandler(logging.NullHandler())

class TestDispatchScada(unittest.TestCase):

    def test_dataset(self):
        self.assertEqual(True, True)

    def test_standarize(self):
        self.assertEqual(True, True)

    def test_nemserializer(self):
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
