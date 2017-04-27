from django.shortcuts import render
from django.http import HttpResponse
from .models import Epocher

Ep = Epocher()

# Create your views here.
def epochTime(request):
    # return HttpResponse('HUJ !!')
    epTime = Ep.getEpochTime(0)
    return render(request, 'epoch/screen01.html', {'epTime': epTime})
