import unittest
from method.crossover import pmx


class CrossoverTestCase(unittest.TestCase):
    def setUp(self):
        self.test_array = ([1, 2, 3, 4, 5, 6, 7], [5, 4, 6, 7, 2, 1, 3])

    def test_pmx(self):
        # for testing, don't forget
        # set point1, point2 = 2, 5
        self.assertEqual(
            ([3, 5, 6, 7, 2, 1, 4], [2, 7, 1, 4, 5, 3, 6]),
            pmx(self.test_array[0], self.test_array[1])
        )


if __name__ == '__main__':
    unittest.main()
