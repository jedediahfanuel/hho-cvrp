import unittest

from optimizers.HHO import get_permutation


class GetPermutationTest(unittest.TestCase):
    def setUp(self):
        self.arr = [0.1, 0.5, 0.3, 0.7, 0.2]
        self.res = [0, 4, 2, 1, 3]

    def test_get_permutation(self):
        self.assertEqual(
            self.res,
            get_permutation(self.arr)
        )


if __name__ == '__main__':
    unittest.main()
