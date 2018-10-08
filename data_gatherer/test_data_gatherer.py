"""Tests for the data_gatherer module."""

from . import data_gatherer
import Config
import unittest


class TestCallSearchApi(unittest.TestCase):

    def test_generalTicker(self):
        actual = data_gatherer._callSearchApi(['MSFT'], Config.API_KEY)
        expected = {'MSFT': 'Microsoft Corporation'}
        self.assertDictEqual(actual, expected)

    def test_dotTicker(self):
        with self.assertRaises(IOError):
            data_gatherer._callSearchApi(['BRK.A'], Config.API_KEY)


if __name__ == '__main__':
    unittest.main()
