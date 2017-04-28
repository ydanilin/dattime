from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import Epocher


class Form_inscription(forms.Form):
    day = forms.CharField(label="Day", max_length=30)
    month = forms.ChoiceField(label='Month', choices=[(1, 'Jan'), (2, 'Feb')])


Ep = Epocher()

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
        form = Form_inscription(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            return HttpResponse("Developer added")
        else:
            return render(request, 'epoch/birthday.html',
                          {'footerItems': footerItems, 'form' : form})
    else:
        form = Form_inscription()
        return render(request, 'epoch/birthday.html',
                      {'footerItems': footerItems, 'form': form})


def bridge(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[3]]
    return render(request, 'epoch/bridge.html', {'footerItems': footerItems})

def calculation(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[2]]
    return render(request, 'epoch/calculation.html', {'footerItems': footerItems})