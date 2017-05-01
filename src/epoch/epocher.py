# coding=utf-8
from datetime import datetime, timedelta
from time import gmtime
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
        self.baseHour = 11  # in UTC
        self.baseMinute = 30
        self.wBaseTime = 0  # in world seconds
        self.newSecondRatio = 0.864
        self.ratioMinutes = 10
        self.ratioHours = self.ratioMinutes * 100
        self.ratioDays = self.ratioHours * 100
        self.ratioMonths = self.ratioDays * 100
        self.ratioYears = self.ratioMonths * 10

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
        h = int(timezone)
        m = int(60 * (timezone - h))
        delta = timedelta(hours=h, minutes=m)
        dt = datetime.utcnow() + delta
        return dt

    def worldTimeToEpochSeconds(self, wDt):
        worldSeconds = timegm(wDt.timetuple())
        epSeconds = (worldSeconds - self.wBaseTime) / self.newSecondRatio
        return round(epSeconds, 0)

    def epochSecondsToWorldTime(self, epSeconds):
        worldSeconds = epSeconds*self.newSecondRatio + self.wBaseTime
        dt = datetime.utcfromtimestamp(worldSeconds)
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
        self.adjustBaseTime(timezone)
        wdtMoment = self.todayWorldTime(timezone)
        epMomentSeconds = self.worldTimeToEpochSeconds(wdtMoment)
        epMomentTime = self.epochSecondsToEpochTime(epMomentSeconds)
        wdtDob = datetime(year, month, day, hour, minu, sec)
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
        self.adjustBaseTime(timezone)
        wDt = self.todayWorldTime(timezone)
        epSeconds = self.worldTimeToEpochSeconds(wDt)
        return self.epochSecondsToEpochTime(epSeconds)

    def getEpochDob(self, timezone, year, month, day, hour, minu, sec=0):
        self.adjustBaseTime(timezone)
        wDt = datetime(year, month, day, hour, minu, sec)
        epSeconds = self.worldTimeToEpochSeconds(wDt)
        return self.epochSecondsToEpochTime(epSeconds)

    def getEpochAge(self, timezone, year, month, day, hour, minu, sec=0):
        self.adjustBaseTime(timezone)
        wdtMoment = self.todayWorldTime(timezone)
        wdtDob = datetime(year, month, day, hour, minu, sec)
        epMomentSeconds = self.worldTimeToEpochSeconds(wdtMoment)
        epDobSeconds = self.worldTimeToEpochSeconds(wdtDob)
        epAge = epMomentSeconds - epDobSeconds
        return self.epochSecondsToEpochTime(epAge)

    def getEpochNextDobDate(self, timezone, year, month, day, hour, minu, sec=0):
        epDobSeconds = self.epNextDobSecondsAndEpNowSeconds(timezone, year, month, day, hour, minu, sec)[0]
        return self.epochSecondsToEpochTime(epDobSeconds)

    def getEpochNextDobWorldDate(self, timezone, year, month, day, hour, minu, sec=0):
        epDobSeconds = self.epNextDobSecondsAndEpNowSeconds(timezone, year, month, day, hour, minu, sec)[0]
        return self.epochSecondsToWorldTime(epDobSeconds)

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
