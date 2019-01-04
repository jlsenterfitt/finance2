"""Tests for the data_cleaner module."""

from . import data_cleaner
import config
import numpy as np
import unittest


class TestRemoveFutureData(unittest.TestCase):

    def test_basic(self):
        test_data = {
                'fake': {
                    'price_data': {
                        10: 10.1,
                        11: 11.1,
                        12: 12.1
                        }
                    }
                }
        data_cleaner._removeFutureData(test_data, 11)
        expected = {
                'fake': {
                    'price_data': {
                        10: 10.1
                        }
                    }
                }
        self.assertDictEqual(test_data['fake']['price_data'], expected['fake']['price_data'])


class TestRemoveLowDataTickers(unittest.TestCase):

    def test_basic(self):
        test_data = {
                'fake1': {
                    'price_data': {
                        0: 0
                        }
                    },
                'fake2': {
                    'price_data': {
                        0: 0,
                        1: 1
                        }
                    }
                }
        data_cleaner._removeLowDataTickers(test_data, 2)
        
        self.assertSetEqual(set(test_data.keys()), set(('fake2',)))


class TestRemoveLowDataDays(unittest.TestCase):
    
    def test_basic(self):
        test_data = {
                'fake1': {
                    'price_data': {
                        0: 0
                        }
                    },
                'fake2': {
                    'price_data': {
                        0: 0,
                        1: 1
                        }
                    }
                }
        data_cleaner._removeLowDataDays(test_data)

        self.assertSetEqual(set(test_data['fake1']['price_data'].keys()), set((0,)))
        self.assertSetEqual(set(test_data['fake2']['price_data'].keys()), set((0,)))


class TestConvertToMatrix(unittest.TestCase):

    def test_basic(self):
        test_data = {
                'fake1': {
                    'price_data': {
                        0: 1,
                        1: 2
                        }
                    },
                'fake2': {
                    'price_data': {
                        0: 4,
                        1: 6
                        }
                    }
                }
        (ticker_tuple, return_matrix) = data_cleaner._convertToMatrix(test_data)

        self.assertEqual(ticker_tuple, ('fake1', 'fake2'))
        self.assertEqual(len(return_matrix), 1)
        self.assertTupleEqual(tuple(return_matrix[0]), (2.0, 1.5))


if __name__ == '__main__':
    unittest.main()
