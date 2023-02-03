import unittest

from optimizers.two_opt import swap


class TwoOptCase(unittest.TestCase):
    def setUp(self):
        self.route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_head_swap(self):
        self.assertEqual(
            [4, 3, 2, 1, 0, 5, 6, 7, 8, 9],
            swap(self.route, 0, 4)
        )

    def test_body_swap(self):
        self.assertEqual(
            [0, 1, 6, 5, 4, 3, 2, 7, 8, 9],
            swap(self.route, 2, 6)
        )

    def test_tail_swap(self):
        self.assertEqual(
            [0, 1, 2, 3, 4, 9, 8, 7, 6, 5],
            swap(self.route, 5, 10)
        )


if __name__ == '__main__':
    unittest.main()
