import json
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import Epocher


Ep = Epocher()

# http://stackoverflow.com/questions/32084837/changing-id-of-form-input-element-in-django-when-its-created
class Form_inscription(forms.Form):
    timezone = forms.ChoiceField(label="Time zone", choices=[(0, 'GMT'),
                                                             (1, 'GMT+1'),
                                                             (2, 'GMT+2')
                                                             ])
    day = forms.IntegerField(label="Day", min_value=1, max_value=31)
    month = forms.ChoiceField(label='Month', choices=[(1, 'Jan'), (2, 'Feb'),
                                                      (3, 'Mar'), (4, 'Apr'),
                                                      (5, 'May'), (6, 'Jun'),
                                                      (7, 'Jul'), (8, 'Aug'),
                                                      (9, 'Sep'), (10, 'Oct'),
                                                      (11, 'Nov'), (12, 'Dec')])
    year = forms.IntegerField(label="Year")
    hour = forms.IntegerField(label="Hour", min_value=0, max_value=23)
    minute = forms.IntegerField(label="Minute", min_value=0, max_value=59)

menuSet = [{'caption': 'Homepage', 'viewName': 'epochTime'},
           {'caption': 'My Birthday in the New Epoch', 'viewName': 'birthday'},
           {'caption': 'The Bridge between calendars', 'viewName': 'bridge'},
           {'caption': 'The New Time', 'viewName': 'calculation'}]


def epochTime(request):
    # return HttpResponse('HUJ !!')
    footerItems = [menuSet[1], menuSet[2], menuSet[3]]
    epTime = Ep.getEpochTime(0)
    return render(request, 'epoch/screen01.html', {'epTime': epTime,
                                                   'footerItems': footerItems})


def birthday(request):
    footerItems = [menuSet[0], menuSet[2], menuSet[3]]
    if request.POST:
        timezone = int(request.POST.get('timezone'))
        day = int(request.POST.get('day'))
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))

        output = dict(epDob=Ep.getEpochDob(timezone, year, month, day, hour, minute),
                      epAge=Ep.getEpochAge(timezone, year, month, day, hour, minute),
                      epNextDob=Ep.getEpochNextDobDate(timezone, year, month, day, hour, minute),
                      wNextDob=Ep.getEpochNextDobWorldDate(timezone, year, month, day, hour, minute).isoformat()
                      )

        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )
    else:
        # this is on page load
        form = Form_inscription()
        return render(request, 'epoch/birthday.html',
                      {'footerItems': footerItems, 'form': form})


def bridge(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[3]]

    if request.POST:
        timezone = int(request.POST.get('timezone'))
        day = int(request.POST.get('day'))
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        hour = int(request.POST.get('hour'))
        minute = int(request.POST.get('minute'))
        output = Ep.getEpochEventDate(timezone, year, month, day, hour, minute)
        return HttpResponse(
            json.dumps(output),
            content_type="application/json"
        )
    else:
        form = Form_inscription()
        return render(request, 'epoch/bridge.html',
                      {'footerItems': footerItems, 'form': form})


def calculation(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[2]]
    return render(request, 'epoch/calculation.html',
                  {'footerItems': footerItems})
