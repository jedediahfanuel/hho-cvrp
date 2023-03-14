import cvrplib
import random
import unittest

from method.local import two_opt_inverse


class TwoOptCase(unittest.TestCase):
    def setUp(self):
        self.instance, self.sol = cvrplib.download("A-n32-k5", solution=True)

    def test_two_opt_0(self):
        self.assertIn(
            two_opt_inverse(
                [0] + random.sample(self.sol.routes[0], len(self.sol.routes[0])) + [0],
                self.instance.distances
            ),
            [
                [0] + self.sol.routes[0] + [0],
                [0] + self.sol.routes[0][::-1] + [0]
            ]
        )

    def test_two_opt_1(self):
        self.assertIn(
            two_opt_inverse(
                [0] + random.sample(self.sol.routes[1], len(self.sol.routes[1])) + [0],
                self.instance.distances
            ),
            [
                [0] + self.sol.routes[1] + [0],
                [0] + self.sol.routes[1][::-1] + [0]
            ]
        )

    def test_two_opt_2(self):
        self.assertIn(
            two_opt_inverse(
                [0] + random.sample(self.sol.routes[2], len(self.sol.routes[2])) + [0],
                self.instance.distances
            ),
            [
                [0] + self.sol.routes[2] + [0],
                [0] + self.sol.routes[2][::-1] + [0]
            ]
        )

    def test_two_opt_3(self):
        self.assertIn(
            two_opt_inverse(
                [0] + random.sample(self.sol.routes[3], len(self.sol.routes[3])) + [0],
                self.instance.distances
            ),
            [
                [0] + self.sol.routes[3] + [0],
                [0] + self.sol.routes[3][::-1] + [0]
            ]
        )

    def test_two_opt_4(self):
        self.assertIn(
            two_opt_inverse(
                [0] + random.sample(self.sol.routes[4], len(self.sol.routes[4])) + [0],
                self.instance.distances
            ),
            [
                [0] + self.sol.routes[4] + [0],
                [0] + self.sol.routes[4][::-1] + [0]
            ]
        )


if __name__ == '__main__':
    unittest.main()
