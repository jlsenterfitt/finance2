"""Tests for the data_cleaner module."""

from . import trader
import config
import numpy as np
import unittest


class TestGetBacktestedReturns(unittest.TestCase):

    def test_basic(self):
        allocation_map = {
                'fake1': 0.25,
                'fake2': 0.75
                }
        ticker_tuple = ('fake1', 'fake2')
        data_matrix = np.array(
                [
                    [0, 1],
                    [0, 2],
                    [1, 2]
                    ],
                dtype=np.float64)
        expected = [0.75, 1.5, 1.75]
        actual = trader._getBacktestedAllocationReturns(allocation_map, ticker_tuple, data_matrix)

        self.assertListEqual(list(actual), expected)

