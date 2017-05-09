import unittest
from ..epoch import Epocher


class SpaceAge_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()

    def test_getEpochAge(self):
        pass

if __name__ == '__main__':
    unittest.main()
