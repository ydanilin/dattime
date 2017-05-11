import unittest
from ..epoch import Epocher


class EpochToAretz_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()

    def test_getEventUserDateUTC3(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(3, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T09:57:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTC9(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T15:57:53 UTC+9
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(9, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T15:57:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTC12(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T18:57:53 UTC+12
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(12, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T18:57:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTC545(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T12:42:53 UTC+5:45
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(5.75, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T12:42:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTC530(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T12:27:53 UTC+5:30
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(5.5, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T12:27:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTC0(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T06:57:53 UTC+0
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(0, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T06:57:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTCminus9(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-08T21:57:53 UTC-9
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(-9, 14, 9, 8, 85, 27, 1)
        test = '2017-05-08T21:57:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTCminus12(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-08T18:57:53 UTC-12
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(-12, 14, 9, 8, 85, 27, 1)
        test = '2017-05-08T18:57:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTCminus545(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T01:12:53 UTC-5:45
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(-5.75, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T01:12:53'
        self.assertEqual(output, test)

    def test_getEventUserDateUTCminus530(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T01:27:53 UTC-5:30
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getEventUserDate(-5.5, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T01:27:53'
        self.assertEqual(output, test)

if __name__ == '__main__':
    unittest.main()
