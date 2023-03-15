import unittest

from method.local_search import inverse


class InverseCase(unittest.TestCase):
    def setUp(self):
        self.route = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def test_head_inverse(self):
        self.assertEqual(
            [0, 4, 3, 2, 1, 5, 6, 7, 8, 9],
            inverse(self.route, 0, 4)
        )

    def test_body_inverse(self):
        self.assertEqual(
            [0, 1, 2, 6, 5, 4, 3, 7, 8, 9],
            inverse(self.route, 2, 6)
        )

    def test_tail_inverse(self):
        self.assertEqual(
            [0, 1, 2, 3, 4, 5, 9, 8, 7, 6],
            inverse(self.route, 5, 9)
        )


if __name__ == '__main__':
    unittest.main()
