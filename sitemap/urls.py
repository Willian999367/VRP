#coding: utf-8
from django.urls import path
from django.conf.urls import url
from .import views


urlpatterns = [

    #path('map/', views.Index.as_view(), name='map'),
    url('map/(?P<id>[A-z]+)/$', views.Index.as_view(), name='map'),

]


