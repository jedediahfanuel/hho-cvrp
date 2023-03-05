import unittest
import cvrplib
from benchmarks import split_customer
from optimizers.hho_cvrp import cvrp_two_opt_no_depot


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.data = cvrplib.download("A-n32-k5")
        self.test_list = [
            30, 26, 16, 12, 1, 7, 13, 21,
            31, 19, 17, 6, 2, 3, 23, 28,
            4, 11, 8, 18, 9, 22, 15, 10,
            25, 29, 5, 20, 27, 24, 14
        ]
        self.vrp = [
            [0, 30, 12, 1, 7, 16, 26, 0],
            [0, 13, 21, 31, 19, 17, 6, 0],
            [0, 2, 3, 23, 28, 4, 11, 8, 18, 0],
            [0, 29, 22, 9, 15, 10, 25, 5, 20, 0],
            [0, 27, 24, 14, 0]
        ]
        self.tsp = [
            30, 12, 1, 7, 16, 26,
            13, 21, 31, 19, 17, 6,
            2, 3, 23, 28, 4, 11, 8, 18,
            29, 22, 9, 15, 10, 25, 5, 20,
            27, 24, 14,
        ]

    def test_cvrp_two_opt(self):
        x = cvrp_two_opt_no_depot(
            split_customer(self.test_list, self.data.capacity, self.data.demands),
            self.data.distances
        )
        self.assertEqual(self.tsp, x)

    def test_split(self):
        x = split_customer(cvrp_two_opt_no_depot(
            split_customer(self.test_list, self.data.capacity, self.data.demands),
            self.data.distances
        ), self.data.capacity, self.data.demands)
        self.assertEqual(self.vrp, x)


if __name__ == '__main__':
    unittest.main()
