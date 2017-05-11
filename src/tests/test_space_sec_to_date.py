import unittest
from ..epoch import Epocher


class Epocher_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()
        cls.max32bit = 2147483647

    def test_spaceSecToSpaceDate_MAX32(self):
        output = self.ep.spaceSecondsToDate(self.max32bit)
        test = dict(Year=21, Month=4, Day=74,
                    Hour=83, Minute=64, Second=7,
                    Direction=1)
        self.assertEqual(output, test)

    def test_spaceSecToSpaceDate_aboveMAX32(self):
        output = self.ep.spaceSecondsToDate(self.max32bit + 700000000)
        test = dict(Year=28, Month=4, Day=74,
                    Hour=83, Minute=64, Second=7,
                    Direction=1)
        self.assertEqual(output, test)

    def test_spaceSecToSpaceDate_minusMAX32(self):
        output = self.ep.spaceSecondsToDate(-self.max32bit - 1)
        test = dict(Year=21, Month=4, Day=74,
                    Hour=83, Minute=64, Second=8,
                    Direction=-1)
        self.assertEqual(output, test)

    def test_spaceSecToSpaceDate_belowMinusMAX32(self):
        output = self.ep.spaceSecondsToDate(-self.max32bit - 1 - 700000000)
        test = dict(Year=28, Month=4, Day=74,
                    Hour=83, Minute=64, Second=8,
                    Direction=-1)
        self.assertEqual(output, test)

    def test_spaceSecToSpaceDate_zero(self):
        output = self.ep.spaceSecondsToDate(0)
        test = dict(Year=0, Month=0, Day=0,
                    Hour=0, Minute=0, Second=0,
                    Direction=1)
        self.assertEqual(output, test)


if __name__ == '__main__':
    unittest.main()
