import unittest

from method.extra.encode import rke


class EncodeTest(unittest.TestCase):
    def setUp(self):
        self.arr = [0.1, 0.5, 0.3, 0.7, 0.2]
        self.result = [1, 4, 3, 5, 2]

    def test_random_key(self):
        self.assertEqual(
            self.result,
            rke(self.arr)
        )


if __name__ == '__main__':
    unittest.main()
