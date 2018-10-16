"""Tests for the data_gatherer module."""

from . import data_gatherer
import config
import os
import unittest


def _validateDataFormat(self, data):
    self.assertEqual(len(data.keys()), 1)
    self.assertEqual(list(data)[0], 'MSFT')
    self.assertSetEqual(set(data['MSFT'].keys()), {'name', 'price_data'})


class TestCallSearchApi(unittest.TestCase):

    def test_generalTicker(self):
        actual = data_gatherer._callSearchApi('MSFT', config.API_KEY)
        expected = 'Microsoft Corporation'
        self.assertEqual(actual, expected)

    def test_badTicker(self):
        with self.assertRaises(IOError):
            data_gatherer._callSearchApi('ABCXYZ', config.API_KEY)


class TestCallDailyAdjustedApi(unittest.TestCase):

    def test_generalTicker(self):
        actual = data_gatherer._callDailyAdjustedApi('MSFT', config.API_KEY)
        for k, v in actual.items():
            self.assertIsInstance(k, int)
            self.assertIsInstance(v, float)

    def test_badTicker(self):
        with self.assertRaises(IOError):
            data_gatherer._callDailyAdjustedApi('ABCXYZ', config.API_KEY)


class TestGetAllApiData(unittest.TestCase):

    def test_generalTicker(self):
        actual = data_gatherer._getAllApiData('MSFT', config.API_KEY)
        _validateDataFormat(self, actual)


class TestWriteCache(unittest.TestCase):

    def test_generalTicker(self):
        if os.path.isfile('cache/MSFT.json.bz2'):
            os.remove('cache/MSFT.json.bz2')
        data_gatherer._getAndCacheApiData(['MSFT'], config.API_KEY, 'cache')
        self.assertTrue(os.path.isfile('cache/MSFT.json.bz2'))


class TestReadCache(unittest.TestCase):

    def test_generalTicker(self):
        data_gatherer._getAndCacheApiData(['MSFT'], config.API_KEY, 'cache')
        actual = data_gatherer._readCacheFile('MSFT', 'cache')
        _validateDataFormat(self, actual)


if __name__ == '__main__':
    unittest.main()
