import unittest
from datetime import datetime
from ..epoch import Epocher


class AnnualEventDetails_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()
        # for testing, all user time MUST be in UTC+0
        cls.mDt = datetime(2017, 5, 11, 10, 30)  # 13:30
        # BC = Before Christ
        cls.eventBC = dict(Year=0, Month=2, Day=47,
                    Hour=0, Minute=0, Second=0, Direction=-1)
        cls.ageBC = dict(Year=15, Month=1, Day=58,
                    Hour=0, Minute=0, Second=0, Direction=1)
        cls.daysBC = dict(Year=0, Month=8, Day=42,
                    Hour=0, Minute=0, Second=0, Direction=1)
        cls.nextEventBC = dict(Year=15, Month=7, Day=53,
                    Hour=0, Minute=0, Second=0, Direction=1)

    def test_getSpaceMoment(self):
        output = self.ep.getSpaceMoment(self.mDt)
        test = dict(Year=14, Month=9, Day=11,
                    Hour=0, Minute=0, Second=0, Direction=1)
        self.assertEqual(output, test)

    def test_getAnnualEventDetails_BC_UTC3(self):
        output = self.ep.getAnnualEventDetails(3, self.mDt, 1975, 11, 10, 13, 30)
        self.assertEqual(output[0], self.eventBC)
        self.assertEqual(output[1], self.ageBC)
        self.assertEqual(output[2], self.daysBC)
        self.assertEqual(output[3], self.nextEventBC)
        self.assertEqual(output[4].isoformat(), '2019-08-31T13:30:00')

    def test_getAnnualEventDetails_BC_UTC9(self):
        output = self.ep.getAnnualEventDetails(9, self.mDt, 1975, 11, 10, 19, 30)
        self.assertEqual(output[0], self.eventBC)
        self.assertEqual(output[1], self.ageBC)
        self.assertEqual(output[2], self.daysBC)
        self.assertEqual(output[3], self.nextEventBC)
        self.assertEqual(output[4].isoformat(), '2019-08-31T19:30:00')

    def test_getAnnualEventDetails_BC_UTC545(self):
        output = self.ep.getAnnualEventDetails(5.75, self.mDt, 1975, 11, 10, 16, 15)
        self.assertEqual(output[0], self.eventBC)
        self.assertEqual(output[1], self.ageBC)
        self.assertEqual(output[2], self.daysBC)
        self.assertEqual(output[3], self.nextEventBC)
        self.assertEqual(output[4].isoformat(), '2019-08-31T16:15:00')

    def test_getAnnualEventDetails_BC_UTCminus545(self):
        output = self.ep.getAnnualEventDetails(-5.75, self.mDt, 1975, 11, 10, 4, 45)
        self.assertEqual(output[0], self.eventBC)
        self.assertEqual(output[1], self.ageBC)
        self.assertEqual(output[2], self.daysBC)
        self.assertEqual(output[3], self.nextEventBC)
        self.assertEqual(output[4].isoformat(), '2019-08-31T04:45:00')

    def test_getAnnualEventDetails_BC_UTCminus12(self):
        output = self.ep.getAnnualEventDetails(-12, self.mDt, 1975, 11, 9, 22, 30)
        self.assertEqual(output[0], self.eventBC)
        self.assertEqual(output[1], self.ageBC)
        self.assertEqual(output[2], self.daysBC)
        self.assertEqual(output[3], self.nextEventBC)
        self.assertEqual(output[4].isoformat(), '2019-08-30T22:30:00')


if __name__ == '__main__':
    unittest.main()
