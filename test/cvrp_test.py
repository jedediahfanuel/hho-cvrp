import unittest
import cvrplib
import benchmarks


class CvrpTest(unittest.TestCase):
    def setUp(self):
        self.data, self.sol = cvrplib.download("A-n32-k5", solution=True)

    def test_normal_cvrp(self):
        test_routes = [
            [0, 30, 26, 16, 7, 1, 12, 0],
            [0, 13, 21, 31, 19, 17, 6, 0],
            [0, 2, 3, 23, 28, 4, 11, 8, 18, 0],
            [0, 22, 9, 15, 29, 10, 25, 5, 20, 0],
            [0, 27, 24, 14, 0]
        ]
        self.assertEqual(
            822,
            benchmarks.normal_cvrp(
                test_routes,
                self.data.distances
            )
        )

    def test_a_n32_k5(self):
        self.assertEqual(
            self.sol.cost,
            benchmarks.normal_cvrp(
                [[0] + route + [0] for route in self.sol.routes],
                self.data.distances
            )
        )


if __name__ == '__main__':
    unittest.main()
