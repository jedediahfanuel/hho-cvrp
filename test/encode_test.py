import unittest

from method.encode import random_key_original
from method.encode import random_key


class EncodeTest(unittest.TestCase):
    def setUp(self):
        self.arr = [0.1, 0.5, 0.3, 0.7, 0.2]
        self.result_original = [1, 5, 3, 2, 4]
        self.result = [1, 4, 3, 5, 2]

    def test_random_key_original(self):
        self.assertEqual(
            self.result_original,
            random_key_original(self.arr)
        )

    def test_random_key(self):
        self.assertEqual(
            self.result,
            random_key(self.arr)
        )


if __name__ == '__main__':
    unittest.main()
