# coding=utf-8
from math import modf
from datetime import datetime, timedelta
from pytz import country_timezones, timezone
from prettytable import PrettyTable


out = PrettyTable(['Name', 'UTC shift', 'TZ abbrev'])
# https://code.google.com/archive/p/prettytable/wikis/Tutorial.wiki
out.align['Name'] = 'l'
date = datetime(2017, 5, 11)
# country codes:
# https://www.iso.org/obp/ui/#search
countryCode = 'RU'
tzrange = country_timezones(countryCode)
tzAmt = len(tzrange)
print('{0} has {1} timezones'.format(countryCode, tzAmt))
print('They are:')
for tzName in tzrange:
    tz = timezone(tzName)
    shift = tz.utcoffset(date, is_dst=True)
    seconds = shift.seconds
    if shift.days < 0:
        seconds -= 86400
    m, h = modf(seconds/3600)
    h = int(h)
    m = abs(int(m*60))
    shiftStr = '{}:{:02d}'.format(h, m)
    out.add_row([tzName, shiftStr, tz.tzname(date, is_dst=True)])

print(out)

# lv = timezone(country_timezones('US')[0])
# print(lv)
# print(type(lv))
# print(lv.tzname(datetime(1985, 6, 25, 23, 30)))
