import unittest
from datetime import datetime
from ..epoch import Epocher


class Epocher_Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ep = Epocher()

    # def test_adjustBaseTime(self):
    #     # zero
    #     self.ep.adjustBaseTime(0)
    #     dat = datetime.utcfromtimestamp(self.ep.wBaseTime)
    #     dtext = dat.isoformat()
    #     self.assertEqual(dtext, '1976-07-14T11:30:00')
    #     # plus 1
    #     self.ep.adjustBaseTime(1)
    #     dat = datetime.utcfromtimestamp(self.ep.wBaseTime)
    #     dtext = dat.isoformat()
    #     self.assertEqual(dtext, '1976-07-14T12:30:00')
    #     # plus 1.5
    #     self.ep.adjustBaseTime(1.5)
    #     dat = datetime.utcfromtimestamp(self.ep.wBaseTime)
    #     dtext = dat.isoformat()
    #     self.assertEqual(dtext, '1976-07-14T13:00:00')
    #     # minus 1
    #     self.ep.adjustBaseTime(-1)
    #     dat = datetime.utcfromtimestamp(self.ep.wBaseTime)
    #     dtext = dat.isoformat()
    #     self.assertEqual(dtext, '1976-07-14T10:30:00')
    #     # minus 1.5
    #     self.ep.adjustBaseTime(-1.5)
    #     dat = datetime.utcfromtimestamp(self.ep.wBaseTime)
    #     dtext = dat.isoformat()
    #     self.assertEqual(dtext, '1976-07-14T10:00:00')

    def test_worldTimeToEpochSecondsTZ2(self):
        """timezone NON-aware"""
        self.ep.adjustBaseTime(0)
        # check against base time
        wdt = datetime(1976, 7, 14, 13, 30)
        es = self.ep.worldTimeToEpochSeconds(wdt)
        self.assertEqual(es, 0)
        # check against date before Christ))
        wdt = datetime(1975, 11, 10, 14, 50)
        es = self.ep.worldTimeToEpochSeconds(wdt)
        self.assertEqual(es, -24694444)
        # check against example in the requirements (1 494 500 000)
        wdt = datetime(2017, 6, 14, 13, 30)
        es = self.ep.worldTimeToEpochSeconds(wdt)
        self.assertEqual(es, 1494500000)
        # get the duration of one new year
        wdt = datetime(1979, 4, 10, 13, 30)
        es = self.ep.worldTimeToEpochSeconds(wdt)
        self.assertEqual(es, 100000000)

    # def test_worldTimeToEpochSecondsTZ0(self):
    #     self.ep.adjustBaseTime(0)
    #     # check against base time
    #     wdt = datetime(1976, 7, 14, 11, 30)
    #     es = self.ep.worldTimeToEpochSeconds(wdt)
    #     self.assertEqual(es, 0)
    #     # check against date before Christ))
    #     wdt = datetime(1975, 11, 10, 12, 50)
    #     es = self.ep.worldTimeToEpochSeconds(wdt)
    #     self.assertEqual(es, -24694444)
    #     # check against example in the requirements (1 494 500 000)
    #     wdt = datetime(2017, 6, 14, 11, 30)
    #     es = self.ep.worldTimeToEpochSeconds(wdt)
    #     self.assertEqual(es, 1494500000)
    #     # get the duration of one new year
    #     wdt = datetime(1979, 4, 10, 11, 30)
    #     es = self.ep.worldTimeToEpochSeconds(wdt)
    #     self.assertEqual(es, 100000000)

    def test_epochSecondsToWorldTime(self):
        """timezone NON-aware"""
        self.ep.adjustBaseTime(0)
        dt = self.ep.epochSecondsToWorldTime(0, 2)
        self.assertEqual(dt.isoformat(), '1976-07-14T13:30:00')
        dt = self.ep.epochSecondsToWorldTime(-24694444, 2)
        self.assertEqual(dt.isoformat(timespec='seconds'), '1975-11-10T14:50:00')
        dt = self.ep.epochSecondsToWorldTime(1494500000, 2)
        self.assertEqual(dt.isoformat(), '2017-06-14T13:30:00')
        dt = self.ep.epochSecondsToWorldTime(100000000, 2)
        self.assertEqual(dt.isoformat(), '1979-04-10T13:30:00')

    def test_epochSecondsToEpochTime(self):
        """timezone NON-aware"""
        self.ep.adjustBaseTime(0)
        output = self.ep.epochSecondsToEpochTime(1494500000)
        self.assertEqual(output, {'Year': 14, 'Month': 9, 'Day': 45,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'FST'})
        output = self.ep.epochSecondsToEpochTime(-1494500000)
        self.assertEqual(output, {'Year': -14, 'Month': -9, 'Day': -45,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'BST'})
        output = self.ep.epochSecondsToEpochTime(0)
        self.assertEqual(output, {'Year': 0, 'Month': 0, 'Day': 0,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'FST'})

    def test_epochTimeToEpochSeconds(self):
        """timezone NON-aware"""
        output = self.ep.epochTimeToEpochSeconds({'Year': -14, 'Month': -9,
                                                  'Day': -45, 'Hour': 0,
                                                  'Minute': 0, 'Second': 0,
                                                  'Direction': 'BST'})
        self.assertEqual(output, -1494500000)
        output = self.ep.epochTimeToEpochSeconds({'Year': 0, 'Month': 0,
                                                  'Day': -31, 'Hour': 0,
                                                  'Minute': 0, 'Second': 0,
                                                  'Direction': 'BST'})
        self.assertEqual(output, -3100000)

    def test_dropYearAndReverseToPositive(self):
        """timezone NON-aware"""
        self.ep.adjustBaseTime(0)
        # this will be one month before Christ, so add year yelds month +9
        wdt = datetime(1976, 4, 5, 13, 30)
        epSeconds = self.ep.worldTimeToEpochSeconds(wdt)
        epTime = self.ep.epochSecondsToEpochTime(epSeconds)
        output = self.ep.dropYearAndReverseToPositive(epTime)
        self.assertEqual(output, {'Year': 0, 'Month': 9, 'Day': 0,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'FST'})
        # this demonstrates how it drops the year
        wdt = datetime(1973, 7, 10, 13, 30)  # -1 year -1 month
        epSeconds = self.ep.worldTimeToEpochSeconds(wdt)
        epTime = self.ep.epochSecondsToEpochTime(epSeconds)
        output = self.ep.dropYearAndReverseToPositive(epTime)
        self.assertEqual(output, {'Year': 0, 'Month': 9, 'Day': 0,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'FST'})

    def test_epNextDobSecondsAndEpNowSeconds(self):
        """timezone AWARE"""
        t = self.ep.epNextDobSecondsAndEpNowSeconds(2, 1975, 11, 10, 13, 30)
        wdt = self.ep.epochSecondsToWorldTime(t[0], 2).isoformat(timespec='seconds')
        # my next stupid birthday will be in 2019
        self.assertEqual(wdt, '2019-08-31T15:29:59')

    def test_getEpochDob_tz0(self):
        output = self.ep.getEpochDob(0, 1975, 11, 10, 11, 30)
        self.assertEqual(output, {'Year': 0, 'Month': -2, 'Day': -47,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'BST'})

    def test_getEpochDob_tz2(self):
        output = self.ep.getEpochDob(2, 1975, 11, 10, 13, 30)
        self.assertEqual(output, {'Year': 0, 'Month': -2, 'Day': -47,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'BST'})

    def test_getEpochDob_tz_minus1d5(self):
        output = self.ep.getEpochDob(-1.5, 1975, 11, 10, 10, 00)
        self.assertEqual(output, {'Year': 0, 'Month': -2, 'Day': -47,
                                  'Hour': 0, 'Minute': 0, 'Second': 0,
                                  'Direction': 'BST'})

    def test_getEpochNextDobDate_tz0(self):
        output = self.ep.getEpochNextDobDate(0, 1975, 11, 10, 11, 30)
        wdt = datetime(2019, 8, 31, 11, 30)
        seconds = self.ep.worldTimeToEpochSeconds(wdt)
        testt = self.ep.epochSecondsToEpochTime(seconds)
        self.assertEqual(output, testt)

    def test_getEpochNextDobDate_tz2(self):
        output = self.ep.getEpochNextDobDate(2, 1975, 11, 10, 13, 30)
        wdt = datetime(2019, 8, 31, 15, 30)
        seconds = self.ep.worldTimeToEpochSeconds(wdt)
        testt = self.ep.epochSecondsToEpochTime(seconds)
        self.assertEqual(output, testt)

    def test_getEpochNextDobDate_tz_minus1d5(self):
        output = self.ep.getEpochNextDobDate(-1.5, 1975, 11, 10, 10, 00)
        wdt = datetime(2019, 8, 31, 8, 30)
        seconds = self.ep.worldTimeToEpochSeconds(wdt)
        testt = self.ep.epochSecondsToEpochTime(seconds)
        self.assertEqual(output, testt)

    def test_getToAltConversionRatios(self):
        output = self.ep.getToAltConversionRatios()
        testDict = dict(rSec=1.157, rMin=6.944, rHour=4.167,
                        rDay=1, rMonth=0.304, rYear=0.365)
        self.assertEqual(output, testDict)

    def test_getToWorldConversionRatios(self):
        output = self.ep.getToWorldConversionRatios()
        testDict = dict(rSec=0.864, rMin=0.144, rHour=0.24,
                        rDay=1, rMonth=3.288, rYear=2.74)
        self.assertEqual(output, testDict)


if __name__ == '__main__':
    unittest.main()
