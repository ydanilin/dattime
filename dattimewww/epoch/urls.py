from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.epochTime, name='epochTime'),
    url(r'^birthday/', views.birthday, name='birthday'),
    url(r'^bridge/', views.bridge, name='bridge'),
    url(r'^calculation/', views.calculation, name='calculation'),
    url(r'^test/', views.testick)
]
