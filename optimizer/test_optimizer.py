"""Tests for the optimizer module."""

from . import optimizer
import config
import numpy as np
import unittest

class TestScoreAllocation(unittest.TestCase):

    def test_positive(self):
        data_matrix = np.array([
                [1.0507, 1.0245],
                [0.9733, 0.9895],
                [0.9793, 0.9846],
                [0.9843, 0.9987],
                [0.9839, 0.9886],
                [0.9993, 1.0013],
                [0.9794, 0.9915],
                [0.9818, 0.9861],
                [0.9976, 0.9986],
                [1.0061, 1.0157]],
            dtype=np.float64)
        allocations = np.array((0.05, 0.95), dtype=np.float64)
        required_return = 0.9950
        expected_score = 0.5430
        optimizer._initializeProcess(data_matrix)
        output = optimizer._scoreAllocation(allocations, required_return)
        self.assertAlmostEqual(output['score'], expected_score, places=4)

    def test_negative(self):
        data_matrix = np.array([
                [1.0507, 1.0245],
                [0.9733, 0.9895],
                [0.9793, 0.9846],
                [0.9843, 0.9987],
                [0.9839, 0.9886],
                [0.9993, 1.0013],
                [0.9794, 0.9915],
                [0.9818, 0.9861],
                [0.9976, 0.9986],
                [1.0061, 1.0157]],
            dtype=np.float64)
        allocations = np.array((0.05, 0.95), dtype=np.float64)
        required_return = 1.0
        expected_score = -0.0024
        optimizer._initializeProcess(data_matrix)
        output = optimizer._scoreAllocation(allocations, required_return)
        self.assertAlmostEqual(output['score'], expected_score, places=4)


if __name__ == '__main__':
    unittest.main()
