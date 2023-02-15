import unittest

from optimizers.encoding import random_key
from optimizers.encoding import random_key_original


class EncodingTest(unittest.TestCase):
    def setUp(self):
        self.arr = [0.1, 0.5, 0.3, 0.7, 0.2]
        self.res = [1, 5, 3, 2, 4]
        self.res_original = [1, 4, 3, 5, 2]

    def test_random_key(self):
        self.assertEqual(
            self.res,
            random_key(self.arr)
        )

    def test_random_key_original(self):
        self.assertEqual(
            self.res_original,
            random_key_original(self.arr)
        )


if __name__ == '__main__':
    unittest.main()
