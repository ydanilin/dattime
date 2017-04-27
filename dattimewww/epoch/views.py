from django.shortcuts import render
from django.http import HttpResponse
from .models import Epocher

Ep = Epocher()

menuSet = [{'caption': 'Homepage', 'viewName': 'epochTime'},
           {'caption': 'My Birthday in the New Epoch', 'viewName': 'birthday'},
           {'caption': 'The Bridge between calendars', 'viewName': 'bridge'},
           {'caption': 'The New Time', 'viewName': 'calculation'}]

# Create your views here.
def epochTime(request):
    # return HttpResponse('HUJ !!')
    footerItems = [menuSet[1], menuSet[2], menuSet[3]]
    epTime = Ep.getEpochTime(0)
    return render(request, 'epoch/screen01.html', {'epTime': epTime,
                                                   'footerItems': footerItems})

def birthday(request):
    footerItems = [menuSet[0], menuSet[2], menuSet[3]]
    return render(request, 'epoch/birthday.html', {'footerItems': footerItems})

def bridge(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[3]]
    return render(request, 'epoch/bridge.html', {'footerItems': footerItems})

def calculation(request):
    footerItems = [menuSet[0], menuSet[1], menuSet[2]]
    return render(request, 'epoch/calculation.html', {'footerItems': footerItems})