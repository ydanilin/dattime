# coding=utf-8
from datetime import datetime, timedelta
from calendar import timegm


class Epocher:
    """
    """
    def __init__(self):
        # print('Epocher instantiated')
        self.baseYear = 1976
        self.baseMonth = 7
        self.baseDay = 14
        self.baseHour = 13  # in UTC+3
        self.baseMinute = 30
        self.baseShift = 3  # UTC+3
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

    def getSubUnits(self):
        return dict(minute=self.ratioMinutes,
                    hour=100,
                    day=100,
                    month=100,
                    year=10)

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

    # **********************************************************
    #        interface functions
    # **********************************************************
    # cleaned
    def getSpaceMoment(self, dt):
        # dt = datetime.utcnow()
        spaceSeconds = self.userDateToSpaceSeconds(0, dt)
        spaceDate = self.spaceSecondsToDate(spaceSeconds)
        return spaceDate

    def getEventSpaceDate(self, shift, year, month, day, hour, minu, sec=0):
        uDt = datetime(year, month, day, hour, minu, sec)
        spaceSeconds = self.userDateToSpaceSeconds(shift, uDt)
        spaceDate = self.spaceSecondsToDate(spaceSeconds)
        return spaceDate

    def getEventUserDate(self, userShift, year, month, day, hour, minu,
                         direction):
        spDate = dict(Second=0, Minute=minu, Hour=hour,
                      Day=day, Month=month, Year=year,
                      Direction=direction)
        spSeconds = self.spaceDateToSeconds(spDate)
        uDt = self.spaceSecondsToUserDate(userShift, spSeconds)
        return uDt.isoformat()

    def getAnnualEventDetails(self, shift, dt, year, month, day, hour, minu, sec=0):
        eventSpaceDate = self.getEventSpaceDate(shift, year, month, day, hour, minu, sec)
        momentSpaceDate = self.getSpaceMoment(dt)
        nextEventDate = self.annualEventNext(eventSpaceDate, momentSpaceDate)
        age = self.spaceTimeDelta(momentSpaceDate, eventSpaceDate)
        daysRemain = self.spaceTimeDelta(nextEventDate, momentSpaceDate)
        nes = self.spaceDateToSeconds(nextEventDate)
        nextEventUserDate = self.spaceSecondsToUserDate(shift, nes)
        return eventSpaceDate, age, daysRemain, nextEventDate, nextEventUserDate

    # refactored
    # forward conversion functions
    def shiftToAretzDate(self, userShift, uDt):
        """input, output = python datetime"""
        h = int(self.baseShift - userShift)
        m = int(60 * (self.baseShift - userShift - h))
        delta = timedelta(hours=h, minutes=m)
        return uDt + delta

    def aretzDateToSeconds(self, aDt):
        return timegm(aDt.timetuple())

    def aretzSecondsToSpaceSeconds(self, aSeconds):
        spaceSeconds = (aSeconds - self.wBaseTime) / self.newSecondRatio
        return round(spaceSeconds, 0)

    # cumulative forward conversion function
    def userDateToSpaceSeconds(self, userShift, uDt):
        aretzDate = self.shiftToAretzDate(userShift, uDt)
        aretzSeconds = self.aretzDateToSeconds(aretzDate)
        spaceSeconds = self.aretzSecondsToSpaceSeconds(aretzSeconds)
        return spaceSeconds

    # backward conversion functions
    def spaceDateToSeconds(self, spDate):
        t = spDate['Second'] + \
            spDate['Minute'] * self.ratioMinutes + \
            spDate['Hour'] * self.ratioHours + \
            spDate['Day'] * self.ratioDays + \
            spDate['Month'] * self.ratioMonths + \
            spDate['Year'] * self.ratioYears
        return t * spDate['Direction']

    def spaceSecondsToAretzSeconds(self, spSeconds):
        aretzSeconds = int(spSeconds * self.newSecondRatio + self.wBaseTime)
        return aretzSeconds

    def aretzSecondsToDate(self, arSeconds):
        if arSeconds < 0:
            aDt = datetime(1970, 1, 1) + timedelta(seconds=arSeconds)
        else:
            aDt = datetime.utcfromtimestamp(arSeconds)
        return aDt

    def shiftToUserDate(self, userShift, aDt):
        h = int(userShift - self.baseShift)
        m = int(60 * (userShift - self.baseShift - h))
        delta = timedelta(hours=h, minutes=m)
        return aDt + delta

    # cumulative backward conversion function
    def spaceSecondsToUserDate(self, userShift, spSeconds):
        arSeconds = self.spaceSecondsToAretzSeconds(spSeconds)
        aDt = self.aretzSecondsToDate(arSeconds)
        uDt = self.shiftToUserDate(userShift, aDt)
        return uDt

    def dropYearAndReverseToPositive(self, spDate):
        spDate['Year'] = 0
        spSeconds = self.spaceDateToSeconds(spDate)
        spSeconds += 100000000  # self.ratioYears
        return self.spaceSecondsToDate(spSeconds)

    # routine to find next annual event
    def annualEventNext(self, eventSpaceDate, momentSpaceDate):
        """ return in seconds """
        if eventSpaceDate['Direction'] == -1:
            eventSpaceDate = self.dropYearAndReverseToPositive(eventSpaceDate)
        # this calculates the event in THIS year
        eventSpaceDate['Year'] = momentSpaceDate['Year']
        eventSec = self.spaceDateToSeconds(eventSpaceDate)
        momentSec = self.spaceDateToSeconds(momentSpaceDate)
        if eventSec < momentSec:
            eventSec += 100000000  # self.ratioYears
        return self.spaceSecondsToDate(eventSec)

    # routine for difference in two space dates
    def spaceTimeDelta(self, minuend, subtrahend):
        left = self.spaceDateToSeconds(minuend)
        right = self.spaceDateToSeconds(subtrahend)
        delta = left - right
        return self.spaceSecondsToDate(delta)

    def spaceSecondsToDate(self, epSeconds):
        direction = 1
        if epSeconds < 0:
            direction = -1
        epSeconds = abs(epSeconds)
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


if __name__ == '__main__':
    ep = Epocher()
