import json
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import Epocher

Ep = Epocher()

tzChoices = [(-12, 'GMT-12'), (-11, 'GMT-11'), (-10, 'GMT-10'),
             (-9, 'GMT-9'), (-8, 'GMT-8'), (-7, 'GMT-7'),
             (-6, 'GMT-6'), (-5, 'GMT-5'), (-4, 'GMT-4'),
             (-3, 'GMT-3'), (-2, 'GMT-2'), (-1, 'GMT-1'),
             (0, 'GMT'),
             (1, 'GMT+1'), (2, 'GMT+2'), (3, 'GMT+3'),
             (4, 'GMT+4'), (5, 'GMT+5'), (5.5, 'GMT+5:30'), (5.75, 'GMT+5:45'),
             (6, 'GMT+6'), (6.5, 'GMT+6:30'),
             (7, 'GMT+7'), (8, 'GMT+8'),
             (9, 'GMT+9'), (9.5, 'GMT+9:30'),
             (10, 'GMT+10'), (11, 'GMT+11'), (12, 'GMT+12')]

monthChoices = [(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'),
                (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'),
                (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')]


# http://stackoverflow.com/questions/32084837/changing-id-of-form-input-element-in-django-when-its-created
class formWorldToAlt(forms.Form):
    def __init__(self, *args, **kwargs):
        super(formWorldToAlt, self).__init__(*args, **kwargs)
        self.initial['timezone'] = 2

    timezone = forms.ChoiceField(label="Time zone", choices=tzChoices)
    day = forms.IntegerField(label="Day", min_value=1, max_value=31)
    month = forms.ChoiceField(label='Month', choices=monthChoices)
    year = forms.IntegerField(label="Year")
    hour = forms.IntegerField(label="Hour", min_value=0, max_value=23)
    minute = forms.IntegerField(label="Minute", min_value=0, max_value=59)


class formAltToWorld(forms.Form):
    def __init__(self, *args, **kwargs):
        super(formAltToWorld, self).__init__(*args, **kwargs)
        self.initial['wtimezone'] = 2
        self.initial['wdirection'] = 1

    wtimezone = forms.ChoiceField(label="Time zone", choices=tzChoices)
    wyear = forms.IntegerField(label="Year")
    wmonth = forms.IntegerField(label='Month', min_value=0, max_value=9)
    wday = forms.IntegerField(label="Day", min_value=0, max_value=99)
    whour = forms.IntegerField(label="Hour", min_value=0, max_value=99)
    wminute = forms.IntegerField(label="Minute", min_value=0, max_value=99)
    wdirection = forms.ChoiceField(label='Direction', choices=[(-1, 'BST'),
                                                               (1, 'FST')])

menuSet = [{'caption': 'Homepage', 'viewName': 'epochTime'},
           {'caption': 'My Birthday in the New Epoch', 'viewName': 'birthday'},
           {'caption': 'The Bridge between calendars', 'viewName': 'bridge'},
           {'caption': 'The New Time', 'viewName': 'calculation'}]


def epochTime(request):
    footerItems = [menuSet[1], menuSet[2], menuSet[3]]
    epTime = Ep.getEpochTime(0)
    return render(request, 'epoch/screen01.html', {'epTime': epTime,
                                                   'footerItems': footerItems})


def birthday(request):
    footerItems = [menuSet[0], menuSet[2], menuSet[3]]
    if request.POST:
        timezone = float(request.POST.get('timezone'))
        print(timezone)
        day = int(request.POST.get('day'))
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))

        output = dict(
            epDob=Ep.getEpochDob(timezone, year, month, day, hour, minute),
            epAge=Ep.getEpochAge(timezone, year, month, day, hour, minute),
            epUntil=Ep.getEpochTimeUntilNextDob(timezone, year, month, day, hour, minute),
            epNextDob=Ep.getEpochNextDobDate(timezone, year, month, day, hour,
                                             minute),
            wNextDob=Ep.getEpochNextDobWorldDate(timezone, year, month, day,
                                                 hour, minute).isoformat()
        )

        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )
    else:
        # this is on page load
        form = formWorldToAlt()
        return render(request, 'epoch/birthday.html',
                      {'footerItems': footerItems, 'form': form})


def bridge(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[3]]

    if request.POST:
        timezone = float(request.POST.get('timezone'))
        day = int(request.POST.get('day'))
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))
        sender = request.POST.get('senderr')
        if sender == 'world':
            output = Ep.getEpochEventDate(timezone, year, month, day, hour, minute)
        if sender == 'alt':
            direction = int(request.POST.get('direction'))
            print(direction)
            output = dict(wtime=Ep.getWorldEventDate(timezone, year, month, day,
                                                     hour, minute, direction))
        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )
    else:
        formW = formWorldToAlt()
        formA = formAltToWorld()
        return render(request, 'epoch/bridge.html',
                      dict(footerItems=footerItems, formW=formW, formA=formA))


def calculation(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[2]]
    toAlt = Ep.getToAltConversionRatios()
    toWorld = Ep.getToWorldConversionRatios()
    units = Ep.getSubUnits()
    return render(request, 'epoch/calculation.html',
                  dict(footerItems=footerItems,
                       toAlt=toAlt,
                       toWorld=toWorld,
                       units=units)
                  )
