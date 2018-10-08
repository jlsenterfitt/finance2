"""Tests for the data_gatherer module."""

from . import data_gatherer
import Config
import unittest


class TestCallSearchApi(unittest.TestCase):

    def test_generalTicker(self):
        actual = data_gatherer._callSearchApi(['MSFT'], Config.API_KEY)
        expected = {'MSFT': 'Microsoft Corporation'}
        self.assertDictEqual(actual, expected)

    def test_badTicker(self):
        with self.assertRaises(IOError):
            data_gatherer._callSearchApi(['BRK.A'], Config.API_KEY)


class TestCallDailyAdjustedApi(unittest.TestCase):

    def test_generalTicker(self):
        actual = data_gatherer._callDailyAdjustedApi(['MSFT'], Config.API_KEY)
        self.assertEqual(len(actual.keys()), 1)
        self.assertEqual(list(actual)[0], 'MSFT')
        for k, v in actual['MSFT'].items():
            self.assertIsInstance(k, int)
            self.assertIsInstance(v, float)

    def test_badTicker(self):
        with self.assertRaises(IOError):
            data_gatherer._callDailyAdjustedApi(['ABCXYZ'], Config.API_KEY)


if __name__ == '__main__':
    unittest.main()
