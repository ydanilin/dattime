import unittest
from ..epoch import Epocher


class AretzToEpoch_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()

    def test_getEventSpaceDateUTC3(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        output = self.ep.getEventSpaceDate(3, 2017, 5, 9, 9, 58)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTC9(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC+9 we must add 9-3=6 hours to the fixed aretz date
        output = self.ep.getEventSpaceDate(9, 2017, 5, 9, 9 + (9 - 3), 58)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTC12(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC+12 we must add 12-3=9 hours to the fixed aretz date
        output = self.ep.getEventSpaceDate(12, 2017, 5, 9, 9 + (12 - 3), 58)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTC545(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC+5:45 we must add 5.45-3=2.45 hours to the fixed aretz date
        # 9:58 -> 12:43
        output = self.ep.getEventSpaceDate(5.75, 2017, 5, 9, 12, 43)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTC530(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC+5:30 we must add 5.30-3=2.30 hours to the fixed aretz date
        # 9:58 -> 12:28
        output = self.ep.getEventSpaceDate(5.5, 2017, 5, 9, 12, 28)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTC0(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC+0 we must add 0-3=-3 hours to the fixed aretz date
        output = self.ep.getEventSpaceDate(0, 2017, 5, 9, 9 + (0 - 3), 58)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTCminus9(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC-9 we must add -9-3=-12 hours to the fixed aretz date
        # 9:58 -> 21:58 previous day
        output = self.ep.getEventSpaceDate(-9, 2017, 5, 8, 21, 58)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTCminus12(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC-12 we must add -12-3=-15 hours to the fixed aretz date
        # 9:58 -> 18:58 previous day
        output = self.ep.getEventSpaceDate(-12, 2017, 5, 8, 18, 58)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTCminus545(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC-5:45 we must add -5.45-3=-8.45 hours to the fixed aretz date
        # 9:58 -> 1:13
        output = self.ep.getEventSpaceDate(-5.75, 2017, 5, 9, 9 - 8, 58 - 45)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)

    def test_getEventSpaceDateUTCminus530(self):
        # Fix the aretz date to 2017-05-09T09:58 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # for UTC+5:30 we must add -5.30-3=-8.30 hours to the fixed aretz date
        # 9:58 -> 1:28
        output = self.ep.getEventSpaceDate(-5.5, 2017, 5, 9, 9 - 8, 58 - 30)
        output['Second'] = 0  # fuck off seconds
        test = dict(Year=14, Month=9, Day=8,
                    Hour=85, Minute=27, Second=0,
                    Direction=1)
        self.assertEqual(output, test)


if __name__ == '__main__':
    unittest.main()
