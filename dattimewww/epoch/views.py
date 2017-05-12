import json
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import Epocher

from django.template import Template, Context


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
        # self.initial['timezone'] = 2

    timezone = forms.ChoiceField(label="Time zone", choices=tzChoices)
    day = forms.IntegerField(label="Day", min_value=1, max_value=31)
    month = forms.ChoiceField(label='Month', choices=monthChoices)
    year = forms.IntegerField(label="Year")
    hour = forms.IntegerField(label="Hour", min_value=0, max_value=23)
    minute = forms.IntegerField(label="Minute", min_value=0, max_value=59)


class formAltToWorld(forms.Form):
    def __init__(self, *args, **kwargs):
        super(formAltToWorld, self).__init__(*args, **kwargs)
        # self.initial['wtimezone'] = 2
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
    # if not request.session.session_key:
    #     request.session.create()
    # print(request.session.session_key)

    footerItems = [menuSet[1], menuSet[2], menuSet[3]]
    dt = datetime.utcnow()
    epTime = Ep.getSpaceMoment(dt)
    return render(request, 'epoch/screen01.html', {'epTime': epTime,
                                                   'footerItems': footerItems})


def birthday(request):
    dt = datetime.utcnow()
    footerItems = [menuSet[0], menuSet[2], menuSet[3]]
    if request.POST:
        timezone = float(request.POST.get('timezone'))
        day = int(request.POST.get('day'))
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))

        event = Ep.getAnnualEventDetails(timezone, dt, year, month, day, hour, minute)

        output = dict(epDob=event[0], epAge=event[1], epUntil=event[2],
                      epNextDob=event[3], wNextDob=event[4].isoformat())
        return HttpResponse(
            json.dumps(output),
            content_type="application/json")
    else:
        # this is on page load
        ini = {}
        if 'country' in request.session:
            if request.session['country'] == 'RU':
                ini = dict(timezone=6)
        form = formWorldToAlt(initial=ini)
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
        output = {}
        if sender == 'world':
            output = Ep.getEventSpaceDate(timezone, year, month, day, hour, minute)
        if sender == 'alt':
            direction = int(request.POST.get('direction'))
            output = dict(wtime=Ep.getEventUserDate(timezone, year, month, day,
                                                    hour, minute, direction))
        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )
    else:
        formW = formWorldToAlt(initial=dict(timezone=3))
        formA = formAltToWorld(initial=dict(wtimezone=3))
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

def testick(request):
    # http://stackoverflow.com/questions/3889769/how-can-i-get-all-the-request-headers-in-django
    t = Template(('<b>request.META</b><br>'
                  '{% for k_meta, v_meta in request.META.items %}'
                  '<code>{{ k_meta }}</code> : {{ v_meta }} <br>'
                  '{% endfor %}'))
    c = Context(dict(request=request))
    return HttpResponse(t.render(c))
