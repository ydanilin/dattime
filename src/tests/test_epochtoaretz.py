import unittest
from ..epoch import Epocher


class EpochToAretz_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()

    def test_getWorldEventDateUTC3(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(3, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T09:57:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTC9(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T15:57:53 UTC+9
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(9, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T15:57:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTC12(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T18:57:53 UTC+12
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(12, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T18:57:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTC545(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T12:42:53 UTC+5:45
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(5.75, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T12:42:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTC530(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T12:27:53 UTC+5:30
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(5.5, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T12:27:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTC0(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T06:57:53 UTC+0
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(0, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T06:57:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTCminus9(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-08T21:57:53 UTC-9
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(-9, 14, 9, 8, 85, 27, 1)
        test = '2017-05-08T21:57:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTCminus12(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-08T18:57:53 UTC-12
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(-12, 14, 9, 8, 85, 27, 1)
        test = '2017-05-08T18:57:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTCminus545(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T01:12:53 UTC-5:45
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(-5.75, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T01:12:53'
        self.assertEqual(output, test)

    def test_getWorldEventDateUTCminus530(self):
        # Fix the aretz date to 2017-05-09T09:57:53 UTC+3 ->
        # 2017-05-09T01:27:53 UTC-5:30
        # This will be Year: 14 Month: 9 Day: 8 Hour: 85 Minute: 27 space date
        # direction 1 = FST, -1 = BST
        output = self.ep.getWorldEventDate(-5.5, 14, 9, 8, 85, 27, 1)
        test = '2017-05-09T01:27:53'
        self.assertEqual(output, test)

if __name__ == '__main__':
    unittest.main()
