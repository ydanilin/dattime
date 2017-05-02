# coding=utf-8
from datetime import datetime, timedelta
from calendar import timegm


class Epocher:
    """
    domain dictionary:
    base: all variables prefixed with "base" are the start of our
          new Sfirat ha-Nocrim
    ep:   prefix "ep" means our New Epoch
    w:    prefix "w" means world regular time counting
    time: all variables containing "time" always expressed in seconds
    """
    def __init__(self):
        # print('Epocher instantiated')
        self.baseYear = 1976
        self.baseMonth = 7
        self.baseDay = 14
        self.baseHour = 13  # in UTC+2
        self.baseMinute = 30
        dt = datetime(self.baseYear,
                      self.baseMonth,
                      self.baseDay,
                      self.baseHour,
                      self.baseMinute)
        self.wBaseTime = timegm(dt.timetuple())  # in world seconds
        self.newSecondRatio = 0.864
        self.ratioMinutes = 10
        self.ratioHours = self.ratioMinutes * 100
        self.ratioDays = self.ratioHours * 100
        self.ratioMonths = self.ratioDays * 100
        self.ratioYears = self.ratioMonths * 10
        self.wMinute = 60
        self.wHour = 60
        self.wDay = 24
        self.wMonth = 30.4167
        self.wYear = 12

    def getToAltConversionRatios(self):
        rSec =    1 / self.newSecondRatio
        rMin =   (1 * self.wMinute) / \
                 (self.newSecondRatio * self.ratioMinutes)
        rHour =  (1 * self.wMinute * self.wHour) / \
                 (self.newSecondRatio * self.ratioHours )
        rDay =   (1 * self.wMinute * self.wHour * self.wDay) / \
                 (self.newSecondRatio * self.ratioDays)
        rMonth = (1 * self.wMinute * self.wHour * self.wDay * self.wMonth) / \
                 (self.newSecondRatio * self.ratioMonths)
        rYear =  (1 * self.wMinute * self.wHour * self.wDay * self.wMonth * self.wYear) / \
                 (self.newSecondRatio * self.ratioYears)
        return dict(rSec=round(rSec, 3), rMin=round(rMin, 3), rHour=round(rHour, 3),
                    rDay=round(rDay, 3), rMonth=round(rMonth, 3), rYear=round(rYear, 3))

    def getToWorldConversionRatios(self):
        rSec =    self.newSecondRatio / 1
        rMin =   (self.newSecondRatio * self.ratioMinutes) / (1 * self.wMinute)
        rHour =  (self.newSecondRatio * self.ratioHours ) / (1 * self.wMinute * self.wHour)
        rDay =   (self.newSecondRatio * self.ratioDays) / (1 * self.wMinute * self.wHour * self.wDay)
        rMonth = (self.newSecondRatio * self.ratioMonths) / (1 * self.wMinute * self.wHour * self.wDay * self.wMonth)
        rYear =  (self.newSecondRatio * self.ratioYears) / (1 * self.wMinute * self.wHour * self.wDay * self.wMonth * self.wYear)
        return dict(rSec=round(rSec, 3), rMin=round(rMin, 3), rHour=round(rHour, 3),
                    rDay=round(rDay, 3), rMonth=round(rMonth, 3), rYear=round(rYear, 3))

    def adjustBaseTime(self, timezone):
        h = int(timezone)
        m = int(60*(timezone - h))
        delta = timedelta(hours=h, minutes=m)
        dt = datetime(self.baseYear,
                      self.baseMonth,
                      self.baseDay,
                      self.baseHour,
                      self.baseMinute) + delta
        self.wBaseTime = timegm(dt.timetuple())

    def todayWorldTime(self, timezone):
        """output in UTC+2"""
        # h = int(2 - timezone)
        # m = int(60 * (2 - timezone - h))
        delta = timedelta(hours=2)#, minutes=m)
        dt = datetime.utcnow() + delta
        # print(dt)
        return dt

    def worldTimeToEpochSeconds(self, wDt):
        """input: datetime ADJUSTED
           output: epoch seconds"""
        worldSeconds = timegm(wDt.timetuple())
        # print(worldSeconds)
        epSeconds = (worldSeconds - self.wBaseTime) / self.newSecondRatio
        return round(epSeconds, 0)

    def epochSecondsToWorldTime(self, epSeconds, timezone):
        worldSeconds = epSeconds*self.newSecondRatio + self.wBaseTime
        h = int(timezone - 2)
        m = int(60 * (timezone - 2 - h))
        delta = timedelta(hours=2, minutes=m)
        dt = datetime.utcfromtimestamp(worldSeconds) #+ delta
        return dt

    def epochSecondsToEpochTime(self, epSeconds):
        direction = 'FST'
        if epSeconds < 0:
            direction = 'BST'
        epYear = int(epSeconds / self.ratioYears)
        t = epSeconds - epYear * self.ratioYears
        epMonth = int(t / self.ratioMonths)
        t = t - epMonth * self.ratioMonths
        epDay = int(t / self.ratioDays)
        t = t - epDay * self.ratioDays
        epHour = int(t / self.ratioHours)
        t = t - epHour * self.ratioHours
        epMinute = int(t / self.ratioMinutes)
        t = t - epMinute * self.ratioMinutes
        epSecond = int(round(t))
        return {'Year': epYear, 'Month': epMonth, 'Day': epDay,
                'Hour': epHour, 'Minute': epMinute, 'Second': epSecond,
                'Direction': direction}

    def epochTimeToEpochSeconds(self, epTime):
        t = epTime['Second'] + \
            epTime['Minute'] * self.ratioMinutes + \
            epTime['Hour'] * self.ratioHours + \
            epTime['Day'] * self.ratioDays + \
            epTime['Month'] * self.ratioMonths + \
            epTime['Year'] * self.ratioYears
        return t

    def dropYearAndReverseToPositive(self, epTime):
        ept = epTime
        ept['Year'] = 0
        seconds = self.epochTimeToEpochSeconds(ept)
        seconds += 100000000
        return self.epochSecondsToEpochTime(seconds)

    def epNextDobSecondsAndEpNowSeconds(self, timezone, year, month, day, hour, minu, sec=0):
        # calculate epMomentSeconds and epDobSeconds
        # self.adjustBaseTime(timezone)
        wdtMoment = self.todayWorldTime(2)
        epMomentSeconds = self.worldTimeToEpochSeconds(wdtMoment)
        epMomentTime = self.epochSecondsToEpochTime(epMomentSeconds)
        # function signature in user timezone. convert to UTC+2
        h = int(2 - timezone)
        m = int(60 * (2 - timezone - h))
        delta = timedelta(hours=h, minutes=m)
        wdtDob = datetime(year, month, day, hour, minu, sec) + delta

        epDobSeconds = self.worldTimeToEpochSeconds(wdtDob)
        # find NEXT epDobSeconds
        epDobTime = self.epochSecondsToEpochTime(epDobSeconds)
        if epDobTime[
            'Direction'] == 'BST':  # check if DobTime before Start and reverse
            epDobTime = self.dropYearAndReverseToPositive(epDobTime)
        epDobTime['Year'] = epMomentTime['Year']
        epDobSeconds = self.epochTimeToEpochSeconds(epDobTime)
        if epDobSeconds < epMomentSeconds:  # if this year Dob past already
            epDobSeconds += 100000000  # move forward to next year
        return epDobSeconds, epMomentSeconds

    # **********************************************************
    #        interface functions
    # **********************************************************
    def getEpochTime(self, timezone):
        # self.adjustBaseTime(timezone)
        wDt = self.todayWorldTime(2)
        epSeconds = self.worldTimeToEpochSeconds(wDt)
        return self.epochSecondsToEpochTime(epSeconds)

    def getEpochDob(self, timezone, year, month, day, hour, minu, sec=0):
        # self.adjustBaseTime(timezone)
        h = int(2 - timezone)
        m = int(60 * (2 - timezone - h))
        delta = timedelta(hours=h, minutes=m)
        wDt = datetime(year, month, day, hour, minu, sec) + delta
        epSeconds = self.worldTimeToEpochSeconds(wDt)
        return self.epochSecondsToEpochTime(epSeconds)

    def getEpochAge(self, timezone, year, month, day, hour, minu, sec=0):
        # self.adjustBaseTime(timezone)
        wdtMoment = self.todayWorldTime(2)
        h = int(2 - timezone)
        m = int(60 * (2 - timezone - h))
        delta = timedelta(hours=h, minutes=m)
        wdtDob = datetime(year, month, day, hour, minu, sec) + delta
        epMomentSeconds = self.worldTimeToEpochSeconds(wdtMoment)
        epDobSeconds = self.worldTimeToEpochSeconds(wdtDob)
        epAge = epMomentSeconds - epDobSeconds
        return self.epochSecondsToEpochTime(epAge)

    def getEpochNextDobDate(self, timezone, year, month, day, hour, minu, sec=0):
        epDobSeconds = self.epNextDobSecondsAndEpNowSeconds(timezone, year, month, day, hour, minu, sec)[0]
        return self.epochSecondsToEpochTime(epDobSeconds)

    def getEpochNextDobWorldDate(self, timezone, year, month, day, hour, minu, sec=0):
        epDobSeconds = self.epNextDobSecondsAndEpNowSeconds(timezone, year, month, day, hour, minu, sec)[0]
        dt = self.epochSecondsToWorldTime(epDobSeconds, timezone)
        h = int(timezone - 2)
        m = int(60 * (timezone - 2 - h))
        delta = timedelta(hours=h, minutes=m)
        return dt + delta

    def epochDaysToNextDob(self, timezone, year, month, day, hour, minu, sec=0):
        epDobSeconds, epMomentSeconds = self.epNextDobSecondsAndEpNowSeconds(timezone, year, month, day, hour, minu, sec)
        diff = epDobSeconds - epMomentSeconds
        return self.epochSecondsToEpochTime(diff)

    def getEpochEventDate(self, timezone, year, month, day, hour, minu, sec=0):
        return self.getEpochDob(timezone, year, month, day, hour, minu, sec)

if __name__ == '__main__':
    ep = Epocher()
    ep.adjustBaseTime(0)
    print(datetime.utcfromtimestamp(ep.wBaseTime))
    print(ep.todayWorldTime(0))
    epSec = ep.worldTimeToEpochSeconds(datetime(1972, 7, 14, 14, 30))
    print(epSec)
    epT = ep.epochSecondsToEpochTime(epSec)
    print(epT)
    print(ep.epochTimeToEpochSeconds(epT))
    print('Epoch Age', ep.getEpochAge(0, 1975, 11, 10, 12, 50))
    print('Epoch Dob:', ep.getEpochDob(0, 1975, 11, 10, 12, 50))
    print('Today epoch date:', ep.getEpochTime(0))
    print('Epoch Next Dob', ep.getEpochNextDobDate(0, 1975, 11, 10, 12, 50))
    print('World Next Dob', ep.getEpochNextDobWorldDate(0, 1975, 11, 10, 12, 50))
    print('Epoch days to next Dob', ep.epochDaysToNextDob(0, 1975, 11, 10, 12, 50))
